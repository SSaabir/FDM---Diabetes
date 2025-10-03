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
        """Simplified preprocessing to match actual trained model features"""
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
            
            # Extract categorical inputs
            gender = user_input.get('gender', 'male').lower()
            smoking_history = user_input.get('smoking', 'never').lower()
            
            # Create basic feature set matching the actual model expectations
            features = {
                # Core numerical features (need to be standardized to match training data)
                'age': (age - 45) / 15,  # Simple standardization
                'bmi': (bmi - 25) / 5,   # Simple standardization
                'hbA1c_level': (hba1c_level - 6) / 1,  # Simple standardization
                'blood_glucose_level': (glucose_level - 100) / 30,  # Simple standardization
                
                # Gender encoding (one-hot)
                'gender_Female': gender == 'female',
                'gender_Male': gender == 'male',
                
                # Smoking history encoding (one-hot)
                'smoking_history_No Info': smoking_history == 'no info',
                'smoking_history_current': smoking_history == 'current',
                'smoking_history_ever': smoking_history == 'ever',
                'smoking_history_former': smoking_history == 'former',
                'smoking_history_never': smoking_history == 'never',
                'smoking_history_not current': smoking_history == 'not current',
                
                # BMI categories (one-hot)
                'bmi_category_Normal': 18.5 <= bmi < 25,
                'bmi_category_Obese': bmi >= 30,
                'bmi_category_Overweight': 25 <= bmi < 30,
                'bmi_category_Underweight': bmi < 18.5,
                
                # Age groups (one-hot)
                'age_group_Adult': 18 <= age < 40,
                'age_group_Child': age < 18,
                'age_group_Middle-aged': 40 <= age < 60,
                'age_group_Senior': age >= 60,
                
                # Categorical risk levels (single values, not one-hot)
                'bmi_risk_level': 'overweight' if 25 <= bmi < 30 else 'obese_1' if 30 <= bmi < 35 else 'obese_2' if bmi >= 35 else 'underweight' if bmi < 18.5 else 'normal',
                'age_diabetes_risk': 'very_high_risk' if age >= 65 else 'high_risk' if age >= 50 else 'moderate_risk' if age >= 35 else 'low_risk'
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
                    try:
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
                    except Exception as e:
                        logger.warning(f"ML model prediction failed: {str(e)}, falling back to calculator")
                        # Fallback to risk calculator if model fails
                        risk_probability = self._calculate_risk_with_clinical(features)
                        model_used = "Enhanced Risk Calculator (Clinical + Lifestyle)"
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

    def _calculate_risk_with_clinical(self, features: Dict[str, Any]) -> float:
        """Enhanced risk calculation with clinical data"""
        risk_score = 0.0
        
        # Clinical factors (most important)
        # Convert back from standardized values or use raw if available
        if 'hbA1c_level' in features:
            if isinstance(features['hbA1c_level'], (int, float)) and features['hbA1c_level'] > -10:
                # If standardized, convert back (rough approximation)
                hba1c = features['hbA1c_level'] + 6 if features['hbA1c_level'] < 10 else features['hbA1c_level']
            else:
                hba1c = features['hbA1c_level']
        else:
            hba1c = 5.7
            
        if 'blood_glucose_level' in features:
            if isinstance(features['blood_glucose_level'], (int, float)) and features['blood_glucose_level'] > -10:
                glucose = features['blood_glucose_level'] + 100 if features['blood_glucose_level'] < 10 else features['blood_glucose_level']
            else:
                glucose = features['blood_glucose_level']
        else:
            glucose = 95
        
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
    
    def _calculate_risk_lifestyle_only(self, features: Dict[str, Any]) -> float:
        """Risk calculation based only on lifestyle factors"""
        return self._calculate_lifestyle_risk(features)
    
    def _calculate_lifestyle_risk(self, features: Dict[str, Any]) -> float:
        """Calculate risk from lifestyle and demographic factors"""
        risk_score = 0.0
        
        # Age factor - handle both raw and standardized
        if 'age' in features:
            age = features['age'] + 45 if features['age'] < 10 else features['age']
        else:
            age = 35
            
        if age >= 65:
            risk_score += 0.3
        elif age >= 50:
            risk_score += 0.2
        elif age >= 35:
            risk_score += 0.1
            
        # BMI factor - handle both raw and standardized
        if 'bmi' in features:
            bmi = features['bmi'] + 25 if features['bmi'] < 10 else features['bmi']
        else:
            bmi = 25
            
        if bmi >= 35:
            risk_score += 0.25
        elif bmi >= 30:
            risk_score += 0.2
        elif bmi >= 25:
            risk_score += 0.1
            
        # Gender factor
        if features.get('gender_Male', False):
            risk_score += 0.05
            
        # Smoking history
        if features.get('smoking_history_current', False):
            risk_score += 0.1
        elif features.get('smoking_history_former', False):
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