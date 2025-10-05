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
        self.data_path = Path(__file__).parent.parent.parent / "data" / "processed_enhanced"
        self.women_model = None
        self.men_model = None
        self.women_features = None
        self.men_features = None
        self.feature_scaler = None
        
        self.load_models()
        self.load_scaler()

    def load_models(self):
        """Load gender-specific models with gestational features for women only"""
        try:
            # Load the women-specific model (includes gestational features)
            women_model_path = self.models_path / "diabetes_women_model.pkl"
            if women_model_path.exists():
                self.women_model = joblib.load(women_model_path)
                logger.info(f"✅ Women's model loaded: {women_model_path}")
                
                # Load women's feature schema
                women_features_path = self.models_path / "women_model_features.json"
                if women_features_path.exists():
                    with open(women_features_path, 'r') as f:
                        self.women_features = json.load(f)
                    logger.info(f"✅ Women's features loaded: {len(self.women_features)} features (includes gestational)")
            
            # Load the men-specific model (excludes gestational features)
            men_model_path = self.models_path / "diabetes_men_model.pkl"
            if men_model_path.exists():
                self.men_model = joblib.load(men_model_path)
                logger.info(f"✅ Men's model loaded: {men_model_path}")
                
                # Load men's feature schema
                men_features_path = self.models_path / "men_model_features.json"
                if men_features_path.exists():
                    with open(men_features_path, 'r') as f:
                        self.men_features = json.load(f)
                    logger.info(f"✅ Men's features loaded: {len(self.men_features)} features (no gestational)")
                
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            self.women_model = None
            self.men_model = None

    def load_scaler(self):
        """Load the feature scaler for numeric features - HARDCODED VERSION"""
        try:
            # HARDCODED SCALER - No file dependencies!
            logger.info("🔧 Using hardcoded scaler values")
            
            # Create a simple scaler object with hardcoded values
            class HardcodedScaler:
                def __init__(self):
                    self.feature_names_in_ = ['age', 'bmi', 'hbA1c_level', 'blood_glucose_level']
                    self.mean_ = [41.885856, 27.3207671, 5.527507, 138.05806]
                    self.scale_ = [22.51672729, 6.63675023, 1.07066674, 40.70793251]
                    self.n_features_in_ = 4
                
                def transform(self, X):
                    """Transform features using hardcoded scaler values"""
                    import numpy as np
                    X = np.array(X)
                    return (X - self.mean_) / self.scale_
            
            self.feature_scaler = HardcodedScaler()
            logger.info(f"✅ Hardcoded scaler initialized successfully")
            logger.info(f"✅ Scaler features: {self.feature_scaler.feature_names_in_}")
            logger.info(f"✅ Scaler means: {self.feature_scaler.mean_}")
            logger.info(f"✅ Scaler scales: {self.feature_scaler.scale_}")
            
        except Exception as e:
            logger.error(f"❌ Error initializing hardcoded scaler: {str(e)}")
            self.feature_scaler = None

    def preprocess_input(self, user_input: Dict[str, Any], gender: str) -> Tuple[Dict[str, float], bool]:
        """Gender-specific preprocessing to match trained model features"""
        try:
            # 🔍 DEBUG: Log all input data and types
            logger.info("🔍 DEBUG: Starting preprocess_input with data:")
            for key, value in user_input.items():
                logger.info(f"   {key}: {type(value).__name__} = {value}")
            
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
            
            # Extract categorical inputs - SAFE VERSION
            smoking_raw = user_input.get('smoking', 'never')
            logger.info(f"🔍 DEBUG: smoking_raw type and value: {type(smoking_raw)} = {smoking_raw}")
            
            # Safe conversion to string before calling .lower()
            if isinstance(smoking_raw, bool):
                logger.error(f"🚨 BACKEND: smoking is boolean! Converting {smoking_raw} to string")
                smoking_history = str(smoking_raw).lower()
            else:
                smoking_history = str(smoking_raw).lower()
            
            logger.info(f"🔍 DEBUG: smoking_history after conversion: {smoking_history}")
            
            # Safe gender handling
            logger.info(f"🔍 DEBUG: gender parameter: {type(gender)} = {gender}")
            gender_safe = str(gender).lower()
            
            # Create basic feature set matching the actual model expectations
            features = {
                # Core numerical features (using raw values, models handle scaling)
                'age': age,
                'bmi': bmi,
                'hbA1c_level': hba1c_level,
                'blood_glucose_level': glucose_level,
                
                # Gender encoding (one-hot)
                'gender_Female': gender_safe == 'female',
                'gender_Male': gender_safe == 'male',
                
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
                
                # Default location/demographic features (using most common values)
                'location_Delaware': False,
                'location_Kansas': False,
                'location_Kentucky': False,
                'alcohol_intake_none': True,  # Default assumption
                'region_income_high': True,   # Default assumption
                'year_2019': False,
                'year_2022': True,  # Most recent year
                
                # Categorical risk levels (need to be encoded for XGBoost)
                'bmi_risk_level': 0,  # Will be set with one-hot encoding below
                'age_diabetes_risk': 0  # Will be set with one-hot encoding below
            }
            
            # BMI risk level encoding (one-hot style)
            bmi_risk_categories = ['normal', 'underweight', 'overweight', 'obese_1', 'obese_2']
            if 25 <= bmi < 30:
                bmi_risk = 'overweight'
            elif 30 <= bmi < 35:
                bmi_risk = 'obese_1'
            elif bmi >= 35:
                bmi_risk = 'obese_2'
            elif bmi < 18.5:
                bmi_risk = 'underweight'
            else:
                bmi_risk = 'normal'
            
            # Set BMI risk level as encoded value (0-4)
            features['bmi_risk_level'] = bmi_risk_categories.index(bmi_risk)
            
            # Age diabetes risk encoding (one-hot style)
            age_risk_categories = ['low_risk', 'moderate_risk', 'high_risk', 'very_high_risk']
            if age >= 65:
                age_risk = 'very_high_risk'
            elif age >= 50:
                age_risk = 'high_risk'
            elif age >= 35:
                age_risk = 'moderate_risk'
            else:
                age_risk = 'low_risk'
                
            # Set age diabetes risk as encoded value (0-3)
            features['age_diabetes_risk'] = age_risk_categories.index(age_risk)
            
            # Add gestational history for women only
            if gender_safe == 'female':
                gestational_history_raw = user_input.get('gestationalHistory', 'no')
                logger.info(f"🔍 DEBUG: gestationalHistory_raw type and value: {type(gestational_history_raw)} = {gestational_history_raw}")
                
                # Safe conversion to string before calling .lower()
                if isinstance(gestational_history_raw, bool):
                    logger.error(f"🚨 BACKEND: gestationalHistory is boolean! Converting {gestational_history_raw} to string")
                    gestational_history = str(gestational_history_raw).lower()
                else:
                    gestational_history = str(gestational_history_raw).lower()
                    
                logger.info(f"🔍 DEBUG: gestational_history after conversion: {gestational_history}")
                
                if gestational_history in ['yes', 'true', '1']:
                    features.update({
                        'gestational_history_0.0': False,
                        'gestational_history_1.0': True,
                        'gestational_history_No': False,
                        'gestational_history_Not Applicable': False
                    })
                else:
                    features.update({
                        'gestational_history_0.0': True,
                        'gestational_history_1.0': False,
                        'gestational_history_No': False,
                        'gestational_history_Not Applicable': False
                    })
            
            return features, has_clinical_data
            
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise ValueError(f"Invalid input data: {str(e)}")

    def predict_diabetes_risk(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Gender-specific prediction using XGBoost models with gestational features for women"""
        try:
            # Extract gender first - SAFE VERSION
            gender_raw = user_input.get('gender', 'male')
            logger.info(f"🔍 DEBUG: gender_raw in predict_diabetes_risk: {type(gender_raw)} = {gender_raw}")
            
            # Safe conversion to string before calling .lower()
            if isinstance(gender_raw, bool):
                logger.error(f"🚨 BACKEND: gender is boolean! Converting {gender_raw} to string")
                gender = str(gender_raw).lower()
            else:
                gender = str(gender_raw).lower()
                
            logger.info(f"🔍 DEBUG: gender after conversion: {gender}")
            
            # Preprocess input with gender-specific features
            features, has_clinical_data = self.preprocess_input(user_input, gender)
            
            # Select appropriate gender-specific model
            logger.info(f"🔍 DEBUG: Selecting model for gender: {gender}")
            logger.info(f"🔍 DEBUG: Women model available: {self.women_model is not None}")
            logger.info(f"🔍 DEBUG: Men model available: {self.men_model is not None}")
            
            if gender == 'female' and self.women_model is not None:
                model_to_use = self.women_model
                feature_schema = self.women_features
                model_name = "Women-Specific XGBoost"
                logger.info(f"🔍 DEBUG: Using women's model with {len(feature_schema)} features")
            elif gender == 'male' and self.men_model is not None:
                model_to_use = self.men_model
                feature_schema = self.men_features
                model_name = "Men-Specific XGBoost"
                logger.info(f"🔍 DEBUG: Using men's model with {len(feature_schema)} features")
            else:
                # Fallback if models not available
                logger.warning(f"🚨 DEBUG: No model available for {gender}, using fallback calculator")
                risk_probability = self._calculate_risk_with_clinical(features) if has_clinical_data else self._calculate_risk_lifestyle_only(features)
                model_used = f"Risk Calculator ({'Clinical + Lifestyle' if has_clinical_data else 'Lifestyle Only'})"
                confidence = "moderate"
                
            # Use ML model if available
            if 'model_to_use' in locals():
                try:
                    # Create feature DataFrame with correct schema
                    feature_df = pd.DataFrame([features])
                    
                    # Ensure all required features are present with defaults
                    for col in feature_schema:
                        if col not in feature_df.columns:
                            # Set appropriate defaults for missing features
                            if 'gestational' in col.lower():
                                feature_df[col] = False  # Default gestational features to False
                            elif col in ['gender_Female', 'gender_Male']:
                                feature_df[col] = (col == f'gender_{gender.title()}')
                            else:
                                feature_df[col] = 0  # Default numeric/categorical features
                    
                    # Reorder columns to match training schema
                    feature_df = feature_df[feature_schema]
                    
                    # Apply scaling to numeric features (as models were trained on scaled data)
                    if self.feature_scaler is not None:
                        numeric_features = ['age', 'bmi', 'hbA1c_level', 'blood_glucose_level']
                        
                        # Extract numeric features for scaling
                        numeric_data = feature_df[numeric_features].copy()
                        logger.info(f"🔍 DEBUG: Before scaling - {dict(numeric_data.iloc[0])}")
                        
                        # Apply the scaler
                        scaled_numeric = self.feature_scaler.transform(numeric_data)
                        
                        # Update the feature DataFrame with scaled values
                        feature_df[numeric_features] = scaled_numeric
                        logger.info(f"🔍 DEBUG: After scaling - {dict(feature_df[numeric_features].iloc[0])}")
                    else:
                        logger.warning("⚠️ Feature scaler not available - using raw numeric values")
                    
                    # Make prediction
                    logger.info(f"🔍 DEBUG: Making prediction with feature_df shape: {feature_df.shape}")
                    logger.info(f"🔍 DEBUG: Feature columns: {list(feature_df.columns)}")
                    logger.info(f"🔍 DEBUG: Sample feature values: {dict(list(feature_df.iloc[0].items())[:10])}")
                    
                    prediction_proba = model_to_use.predict_proba(feature_df)
                    logger.info(f"🔍 DEBUG: Raw prediction probabilities: {prediction_proba}")
                    logger.info(f"🔍 DEBUG: Prediction shape: {prediction_proba.shape}")
                    
                    risk_probability = prediction_proba[0][1]
                    logger.info(f"🔍 DEBUG: Extracted risk probability: {risk_probability}")
                    
                    model_used = f"{model_name} Model (Clinical + Lifestyle)"
                    confidence = "high"
                    
                    logger.info(f"✅ Prediction made using {model_name} model: {risk_probability:.4f}")
                    
                except Exception as e:
                    logger.warning(f"❌ ML model prediction failed: {str(e)}, falling back to calculator")
                    # Fallback to risk calculator if model fails
                    risk_probability = self._calculate_risk_with_clinical(features) if has_clinical_data else self._calculate_risk_lifestyle_only(features)
                    model_used = f"Risk Calculator ({'Clinical + Lifestyle' if has_clinical_data else 'Lifestyle Only'})"
                    confidence = "moderate"
            
            # Convert to percentage
            risk_percentage = round(risk_probability * 100, 1)
            logger.info(f"🔍 DEBUG: Final risk calculation:")
            logger.info(f"   - Risk probability: {risk_probability}")
            logger.info(f"   - Risk percentage: {risk_percentage}%")
            logger.info(f"   - Model used: {model_used}")
            
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

            logger.info(f"🔍 DEBUG: Final result - {risk_level} risk ({risk_percentage}%)")

            return {
                "risk_percentage": risk_percentage,
                "risk_level": risk_level,
                "recommendations": recommendations,
                "model_used": model_used,
                "bmi": round(features['bmi'], 2),
                "confidence": confidence,
                "has_clinical_data": has_clinical_data,
                "gender": gender,
                "gestational_features_included": gender == 'female'
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
        logger.info("🔍 DEBUG: Starting _calculate_risk_with_clinical")
        risk_score = 0.0
        
        # Clinical factors (most important)
        # Use raw values directly - no conversion needed
        if 'hbA1c_level' in features:
            hba1c = features['hbA1c_level']
        else:
            hba1c = 5.7
            
        logger.info(f"🔍 DEBUG: HbA1c value: {hba1c}")
            
        if 'blood_glucose_level' in features:
            glucose = features['blood_glucose_level']
        else:
            glucose = 95
            
        logger.info(f"🔍 DEBUG: Glucose value: {glucose}")
        
        # HbA1c scoring (most predictive)
        if hba1c >= 6.5:
            risk_score += 0.7  # Diabetes range
            logger.info(f"🔍 DEBUG: HbA1c >= 6.5, adding 0.7 to risk")
        elif hba1c >= 5.7:
            risk_score += 0.4  # Prediabetes range
            logger.info(f"🔍 DEBUG: HbA1c >= 5.7, adding 0.4 to risk")
        else:
            risk_score += 0.0  # Normal range
            logger.info(f"🔍 DEBUG: HbA1c normal, adding 0.0 to risk")
            
        # Glucose scoring
        if glucose >= 126:  # Fasting glucose diabetes
            risk_score += 0.3
            logger.info(f"🔍 DEBUG: Glucose >= 126, adding 0.3 to risk")
        elif glucose >= 100:  # Prediabetes range
            risk_score += 0.15
            logger.info(f"🔍 DEBUG: Glucose >= 100, adding 0.15 to risk")
            
        logger.info(f"🔍 DEBUG: Risk score after clinical factors: {risk_score}")
            
        # Add lifestyle factors with lower weights
        lifestyle_risk = self._calculate_lifestyle_risk(features) * 0.3
        logger.info(f"🔍 DEBUG: Lifestyle risk component: {lifestyle_risk}")
        risk_score += lifestyle_risk
        
        final_risk = min(risk_score, 0.95)
        logger.info(f"🔍 DEBUG: Final clinical risk (capped at 0.95): {final_risk}")
        
        return final_risk
    
    def _calculate_risk_lifestyle_only(self, features: Dict[str, Any]) -> float:
        """Risk calculation based only on lifestyle factors"""
        return self._calculate_lifestyle_risk(features)
    
    def _calculate_lifestyle_risk(self, features: Dict[str, Any]) -> float:
        """Calculate risk from lifestyle and demographic factors"""
        logger.info("🔍 DEBUG: Starting _calculate_lifestyle_risk")
        risk_score = 0.0
        
        # Age factor - use raw values directly
        if 'age' in features:
            age = features['age']
        else:
            age = 35
            
        logger.info(f"🔍 DEBUG: Age value: {age}")
            
        if age >= 65:
            risk_score += 0.3
            logger.info(f"🔍 DEBUG: Age >= 65, adding 0.3 to risk")
        elif age >= 50:
            risk_score += 0.2
            logger.info(f"🔍 DEBUG: Age >= 50, adding 0.2 to risk")
        elif age >= 35:
            risk_score += 0.1
            logger.info(f"🔍 DEBUG: Age >= 35, adding 0.1 to risk")
            
        # BMI factor - use calculated BMI directly
        if 'bmi' in features:
            bmi = features['bmi']
        else:
            bmi = 25
            
        logger.info(f"🔍 DEBUG: BMI value: {bmi}")
            
        if bmi >= 35:
            risk_score += 0.25
            logger.info(f"🔍 DEBUG: BMI >= 35, adding 0.25 to risk")
        elif bmi >= 30:
            risk_score += 0.2
            logger.info(f"🔍 DEBUG: BMI >= 30, adding 0.2 to risk")
        elif bmi >= 25:
            risk_score += 0.1
            logger.info(f"🔍 DEBUG: BMI >= 25, adding 0.1 to risk")
            
        # Gender factor
        if features.get('gender_Male', False):
            risk_score += 0.05
            logger.info(f"🔍 DEBUG: Male gender, adding 0.05 to risk")
            
        # Smoking history
        if features.get('smoking_history_current', False):
            risk_score += 0.1
            logger.info(f"🔍 DEBUG: Current smoker, adding 0.1 to risk")
        elif features.get('smoking_history_former', False):
            risk_score += 0.05
            logger.info(f"🔍 DEBUG: Former smoker, adding 0.05 to risk")
        
        final_lifestyle_risk = min(risk_score, 0.8)  # Cap lifestyle-only at 80%
        logger.info(f"🔍 DEBUG: Final lifestyle risk (capped at 0.8): {final_lifestyle_risk}")
        
        return final_lifestyle_risk

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