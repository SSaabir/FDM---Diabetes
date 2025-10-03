import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import logging
import joblib
import json
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class DiabetesPredictionService:
    def __init__(self):
        self.models_path = Path(__file__).parent.parent.parent / "models"
        self.general_model = None
        self.women_model = None
        self.scaler = None
        self.feature_columns = None
        
        self.load_models()

    def load_models(self):
        """Load both general and women-specific models"""
        try:
            # Load the general model
            general_model_path = self.models_path / "diabetes_rf_tuned.pkl"
            if general_model_path.exists():
                self.general_model = joblib.load(general_model_path)
                logger.info(f"✅ General model loaded: {general_model_path}")
            
            # Try to load the women-specific model 
            women_model_path = self.models_path / "diabetes_model.pkl"
            if women_model_path.exists():
                self.women_model = joblib.load(women_model_path)
                logger.info(f"✅ Women model loaded: {women_model_path}")
            
            # Load feature columns
            feature_path = self.models_path / "feature_columns.json"
            if feature_path.exists():
                with open(feature_path, 'r') as f:
                    feature_data = json.load(f)
                    self.feature_columns = feature_data.get('features', [])
                logger.info(f"✅ Feature columns loaded: {len(self.feature_columns)} features")
            
            # Try to load scaler if available
            scaler_path = self.models_path / "../data/processed_enhanced/feature_scaler.pkl"
            scaler_full_path = self.models_path.parent / "data/processed_enhanced/feature_scaler.pkl"
            if scaler_full_path.exists():
                self.scaler = joblib.load(scaler_full_path)
                logger.info("✅ Feature scaler loaded")
                
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            self.general_model = None
            self.women_model = None

    def preprocess_input(self, user_input: Dict[str, Any]) -> Tuple[Dict[str, float], bool]:
        """Enhanced preprocessing to create ML-ready features"""
        try:
            # Extract basic inputs
            age = float(user_input.get('age', 35))
            height = float(user_input.get('height', 170))
            weight = float(user_input.get('weight', 70))
            
            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)
            
            # Check if clinical data is provided
            hba1c = user_input.get('hbA1c')
            glucose = user_input.get('bloodGlucose')
            has_clinical_data = (hba1c is not None and hba1c != '') or (glucose is not None and glucose != '')
            
            # Convert clinical data if provided
            hba1c_level = float(hba1c) if hba1c and hba1c != '' else 5.7  # Default normal value
            glucose_level = float(glucose) if glucose and glucose != '' else 95  # Default normal value
            
            # Extract categorical inputs with proper mapping
            gender = user_input.get('gender', 'male').lower()
            smoking_history = user_input.get('smoking', 'never').lower()
            family_history = user_input.get('familyHistory', 'no').lower()
            hypertension = user_input.get('hypertension', 'no').lower() == 'yes'
            heart_disease = user_input.get('heartDisease', 'no').lower() == 'yes'
            
            # Create comprehensive feature set matching the ML model
            features = {
                # Core numerical features (standardized later)
                'age': age,
                'bmi': bmi, 
                'hbA1c_level': hba1c_level,
                'blood_glucose_level': glucose_level,
                
                # Gender encoding (one-hot)
                'gender_Female': 1 if gender == 'female' else 0,
                'gender_Male': 1 if gender == 'male' else 0,
                
                # Smoking history encoding (one-hot)
                'smoking_history_No Info': 1 if smoking_history == 'no info' else 0,
                'smoking_history_current': 1 if smoking_history == 'current' else 0,
                'smoking_history_ever': 1 if smoking_history == 'ever' else 0,
                'smoking_history_former': 1 if smoking_history == 'former' else 0,
                'smoking_history_never': 1 if smoking_history == 'never' else 0,
                'smoking_history_not current': 1 if smoking_history == 'not current' else 0,
                
                # BMI categories (one-hot)
                'bmi_category_Normal': 1 if 18.5 <= bmi < 25 else 0,
                'bmi_category_Obese': 1 if bmi >= 30 else 0,
                'bmi_category_Overweight': 1 if 25 <= bmi < 30 else 0,
                'bmi_category_Underweight': 1 if bmi < 18.5 else 0,
                
                # Age groups (one-hot)
                'age_group_Adult': 1 if 18 <= age < 40 else 0,
                'age_group_Child': 1 if age < 18 else 0,  # Should not occur with age validation
                'age_group_Middle-aged': 1 if 40 <= age < 60 else 0,
                'age_group_Senior': 1 if age >= 60 else 0,
                
                # BMI risk levels (one-hot)
                'bmi_risk_level_normal': 1 if 18.5 <= bmi < 25 else 0,
                'bmi_risk_level_obese_1': 1 if 30 <= bmi < 35 else 0,
                'bmi_risk_level_obese_2': 1 if bmi >= 35 else 0,
                'bmi_risk_level_overweight': 1 if 25 <= bmi < 30 else 0,
                'bmi_risk_level_underweight': 1 if bmi < 18.5 else 0,
                
                # Age diabetes risk (one-hot)
                'age_diabetes_risk_high_risk': 1 if 50 <= age < 65 else 0,
                'age_diabetes_risk_low_risk': 1 if age < 35 else 0,
                'age_diabetes_risk_moderate_risk': 1 if 35 <= age < 50 else 0,
                'age_diabetes_risk_very_high_risk': 1 if age >= 65 else 0,
            }
            
            return features, has_clinical_data
            
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise ValueError(f"Invalid input data: {str(e)}")

    def predict_diabetes_risk(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced prediction using clinical data when available"""
        try:
            # Preprocess input and check for clinical data
            features, has_clinical_data = self.preprocess_input(user_input)
            
            # Select appropriate model and determine confidence
            gender = user_input.get('gender', 'male').lower()
            
            if has_clinical_data and (self.general_model is not None or self.women_model is not None):
                # Use ML model when clinical data is available
                model_to_use = self.women_model if gender == 'female' and self.women_model else self.general_model
                
                if model_to_use is not None:
                    # Create feature DataFrame in correct order
                    if self.feature_columns:
                        feature_df = pd.DataFrame([features])
                        # Ensure all required features are present
                        for col in self.feature_columns:
                            if col not in feature_df.columns:
                                feature_df[col] = 0
                        # Reorder columns to match training
                        feature_df = feature_df[self.feature_columns]
                    else:
                        feature_df = pd.DataFrame([features])
                    
                    # Make prediction
                    risk_probability = model_to_use.predict_proba(feature_df)[0][1]
                    model_used = f"{'Women-Specific' if gender == 'female' and self.women_model else 'General'} ML Model (Clinical + Lifestyle)"
                    confidence = "high"
                else:
                    # Fallback to risk calculator
                    risk_probability = self._calculate_risk_with_clinical(features)
                    model_used = "Enhanced Risk Calculator (Clinical + Lifestyle)"
                    confidence = "high"
            else:
                # Use lifestyle-only prediction
                risk_probability = self._calculate_risk_lifestyle_only(features)
                model_used = "Lifestyle Risk Calculator (No Clinical Data)"
                confidence = "moderate"
            
            # Convert to percentage
            risk_percentage = round(risk_probability * 100, 1)
            
            # Determine risk level and recommendations
            if risk_percentage < 30:
                risk_level = "low"
                recommendations = self._get_low_risk_recommendations(has_clinical_data)
            elif risk_percentage < 60:
                risk_level = "moderate"
                recommendations = self._get_moderate_risk_recommendations(has_clinical_data)
            else:
                risk_level = "high"
                recommendations = self._get_high_risk_recommendations(has_clinical_data)

            return {
                "risk_percentage": risk_percentage,
                "risk_level": risk_level,
                "recommendations": recommendations,
                "model_used": model_used,
                "bmi": round(features['bmi'], 2),
                "confidence": confidence,
                "has_clinical_data": has_clinical_data
            }

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                "error": f"Prediction failed: {str(e)}",
                "risk_percentage": 0.0,
                "risk_level": "unknown",
                "recommendations": ["Please check your input and try again"],
                "model_used": "Error",
                "bmi": 0.0,
                "confidence": "none",
                "has_clinical_data": False
            }

    def _calculate_risk_with_clinical(self, features: Dict[str, float]) -> float:
        """Enhanced risk calculation with clinical data"""
        risk_score = 0.0
        
        # Clinical factors (most important)
        hba1c = features['hbA1c_level']
        glucose = features['blood_glucose_level']
        
        # HbA1c scoring (most predictive)
        if hba1c >= 6.5:
            risk_score += 0.7  # Diabetes range
        elif hba1c >= 5.7:
            risk_score += 0.4  # Prediabetes range
        else:
            risk_score += 0.0  # Normal range
            
        # Glucose scoring
        if glucose >= 126:  # Fasting glucose diabetes
            risk_score += 0.3
        elif glucose >= 100:  # Prediabetes range
            risk_score += 0.15
            
        # Add lifestyle factors with lower weights
        risk_score += self._calculate_lifestyle_risk(features) * 0.3
        
        return min(risk_score, 0.95)
    
    def _calculate_risk_lifestyle_only(self, features: Dict[str, float]) -> float:
        """Risk calculation based only on lifestyle factors"""
        return self._calculate_lifestyle_risk(features)
    
    def _calculate_lifestyle_risk(self, features: Dict[str, float]) -> float:
        """Calculate risk from lifestyle and demographic factors"""
        risk_score = 0.0
        
        # Age factor
        age = features['age']
        if age >= 65:
            risk_score += 0.3
        elif age >= 50:
            risk_score += 0.2
        elif age >= 35:
            risk_score += 0.1
            
        # BMI factor
        bmi = features['bmi']
        if bmi >= 35:
            risk_score += 0.25
        elif bmi >= 30:
            risk_score += 0.2
        elif bmi >= 25:
            risk_score += 0.1
            
        # Gender factor (from your data, males seem higher risk)
        if features['gender_Male']:
            risk_score += 0.05
            
        # Smoking history
        if features['smoking_history_current']:
            risk_score += 0.1
        elif features['smoking_history_former']:
            risk_score += 0.05
            
        return min(risk_score, 0.8)  # Cap lifestyle-only at 80%

    def _get_low_risk_recommendations(self, has_clinical_data: bool) -> list:
        """Get recommendations for low risk patients"""
        recommendations = [
            "Maintain your healthy lifestyle! 💚",
            "Continue regular physical activity",
            "Keep a balanced diet with limited processed foods",
            "Annual health checkups recommended"
        ]
        
        if has_clinical_data:
            recommendations.append("Your lab values look good - keep monitoring annually")
        else:
            recommendations.append("Consider getting HbA1c and glucose tested annually")
            
        return recommendations

    def _get_moderate_risk_recommendations(self, has_clinical_data: bool) -> list:
        """Get recommendations for moderate risk patients"""
        recommendations = [
            "Focus on lifestyle improvements to reduce risk 👍",
            "Increase physical activity to 150+ minutes/week",
            "Adopt a diabetes-friendly diet (low refined carbs)",
            "Monitor blood glucose levels regularly",
            "Consider weight management if BMI is elevated"
        ]
        
        if has_clinical_data:
            recommendations.append("Discuss lab results with your healthcare provider")
        else:
            recommendations.append("Get HbA1c and glucose testing every 6 months")
            
        return recommendations

    def _get_high_risk_recommendations(self, has_clinical_data: bool) -> list:
        """Get recommendations for high risk patients"""
        recommendations = [
            "⚠️ Consult healthcare provider immediately",
            "Implement intensive lifestyle changes",
            "Daily blood glucose monitoring may be needed",
            "Consider diabetes prevention program enrollment",
            "Regular follow-up with healthcare team"
        ]
        
        if has_clinical_data:
            recommendations.append("Your lab values indicate high risk - immediate medical consultation needed")
        else:
            recommendations.append("Urgent lab testing (HbA1c, glucose) recommended")
            
        return recommendations