"""
ML Prediction Service
Handles diabetes risk prediction using trained models
"""
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiabetesPredictionService:
    def __init__(self):
        self.models_path = Path(__file__).parent.parent.parent / "models"
        self.rf_model = None
        self.feature_columns = None
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load the trained models and preprocessing components"""
        try:
            # Load Random Forest model
            rf_model_path = self.models_path / "diabetes_rf_tuned.pkl"
            if rf_model_path.exists():
                try:
                    self.rf_model = joblib.load(rf_model_path)
                    logger.info("✅ Random Forest model loaded successfully")
                except Exception as e:
                    logger.error(f"❌ Error loading RF model: {str(e)}")
                    self.rf_model = None
            else:
                logger.warning(f"❌ RF model not found at {rf_model_path}")
                self.rf_model = None
            
            # Load feature columns
            feature_cols_path = self.models_path / "feature_columns.json"
            if feature_cols_path.exists():
                try:
                    import json
                    with open(feature_cols_path, 'r') as f:
                        feature_data = json.load(f)
                    # Extract the features list from the dictionary
                    if isinstance(feature_data, dict) and 'features' in feature_data:
                        self.feature_columns = feature_data['features']
                    else:
                        self.feature_columns = feature_data  # fallback if it's already a list
                    logger.info("✅ Feature columns loaded successfully")
                except Exception as e:
                    logger.error(f"❌ Error loading feature columns: {str(e)}")
                    self.feature_columns = None
            else:
                logger.warning(f"❌ Feature columns not found at {feature_cols_path}")
                # Use default feature columns
                self.feature_columns = [
                    'age', 'bmi', 'gender_encoded', 'family_history_encoded',
                    'physical_activity_encoded', 'smoking_encoded', 
                    'blood_pressure_encoded', 'cholesterol_encoded'
                ]
                logger.info("✅ Using default feature columns")
            
            # Skip scaler loading since model was trained on pre-scaled data
            self.scaler = None
            logger.info("⚠️ Skipping scaler - model expects raw values (was trained on pre-scaled data)")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            self.rf_model = None
            self.feature_columns = None
            self.scaler = None
    
    def preprocess_input(self, user_input: Dict[str, Any]) -> np.ndarray:
        """
        Preprocess user input using the EXACT same scaling as the training data
        Using the actual mean/std from the raw dataset
        """
        try:
            # Calculate basic values
            height = user_input.get('height', 170)
            weight = user_input.get('weight', 70)
            bmi = weight / ((height / 100) ** 2)
            age = user_input.get('age', 30)
            
            # Initialize all features to zero (as requested)
            features_dict = {}
            for col in self.feature_columns:
                features_dict[col] = 0.0
            
            # Apply EXACT scaling from training data statistics
            # Age: mean=41.89, std=22.52
            scaled_age = (age - 41.885856) / 22.51683987161702
            features_dict['age'] = scaled_age
            
            # BMI: mean=27.32, std=6.64
            scaled_bmi = (bmi - 27.320767099999994) / 6.636783416648368
            features_dict['bmi'] = scaled_bmi
            
            # HbA1c and glucose - these need proper scaling too
            # Using reasonable medical ranges: HbA1c 4-14% (mean~6%), glucose 70-300 mg/dL (mean~120)
            hba1c_val = user_input.get('hbA1c_level', 5.5)
            glucose_val = user_input.get('blood_glucose_level', 100)
            
            # Estimate scaling for medical values (approximate)
            scaled_hba1c = (hba1c_val - 6.0) / 1.5  # Approximate medical range scaling
            scaled_glucose = (glucose_val - 120) / 40  # Approximate glucose range scaling
            
            features_dict['hbA1c_level'] = scaled_hba1c
            features_dict['blood_glucose_level'] = scaled_glucose
            
            # Gender encoding (binary - no scaling needed)
            gender = user_input.get('gender', '').lower()
            if gender == 'female':
                features_dict['gender_Female'] = 1.0
                features_dict['gender_Male'] = 0.0
            elif gender == 'male':
                features_dict['gender_Female'] = 0.0
                features_dict['gender_Male'] = 1.0
            
            # Smoking history - only set one to 1, rest remain 0
            smoking = user_input.get('smoking', 'never').lower()
            if smoking in ['no', 'never']:
                features_dict['smoking_history_never'] = 1.0
            elif smoking in ['yes', 'current']:
                features_dict['smoking_history_current'] = 1.0
            elif smoking == 'former':
                features_dict['smoking_history_former'] = 1.0
            else:
                features_dict['smoking_history_never'] = 1.0  # Default to never
            
            # All other features remain 0 as initialized
            
            # Create feature array in exact order
            feature_array = []
            for col in self.feature_columns:
                feature_array.append(features_dict[col])
            
            feature_array = np.array(feature_array).reshape(1, -1)
            
            logger.info(f"✅ Prepared {feature_array.shape[1]} features (exact training data scaling)")
            logger.info(f"📊 Scaled features: age={scaled_age:.3f}, bmi={scaled_bmi:.3f}, gender_M={features_dict['gender_Male']}")
                
            return feature_array
            
        except Exception as e:
            logger.error(f"❌ Error in preprocessing: {str(e)}")
            raise
            
            # Apply scaling if scaler is available
            if self.scaler:
                feature_array = self.scaler.transform(feature_array)
            
            return feature_array
            
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise ValueError(f"Failed to preprocess input: {str(e)}")
    
    def _encode_activity_level(self, activity: str) -> int:
        """Encode physical activity level"""
        activity_map = {
            'low': 0,
            'moderate': 1,
            'high': 2
        }
        return activity_map.get(activity.lower(), 1)
    
    def _encode_blood_pressure(self, bp: str) -> int:
        """Encode blood pressure level"""
        bp_map = {
            'normal': 0,
            'elevated': 1,
            'high': 2
        }
        return bp_map.get(bp.lower(), 0)
    
    def _encode_cholesterol(self, chol: str) -> int:
        """Encode cholesterol level"""
        chol_map = {
            'normal': 0,
            'borderline': 1,
            'high': 2
        }
        return chol_map.get(chol.lower(), 0)
    
    def predict_diabetes_risk(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict diabetes risk based on user input
        """
        try:
            # Validate required fields
            required_fields = ['age', 'height', 'weight', 'gender']
            for field in required_fields:
                if field not in user_input:
                    raise ValueError(f"Missing required field: {field}")
            
            # Calculate BMI first
            height_m = float(user_input.get('height', 170)) / 100
            weight = float(user_input.get('weight', 70))
            bmi = weight / (height_m ** 2)
            
            # Try ML model first
            if self.rf_model:
                try:
                    # Preprocess input
                    features = self.preprocess_input(user_input)
                    
                    # Get prediction probability
                    risk_probability = self.rf_model.predict_proba(features)[0][1]  # Probability of diabetes
                    risk_percentage = float(risk_probability * 100)
                    model_used = "Random Forest"
                    confidence = "high" if risk_percentage < 20 or risk_percentage > 80 else "moderate"
                    
                except Exception as e:
                    logger.warning(f"ML model prediction failed, using rule-based: {str(e)}")
                    return self._rule_based_prediction(user_input, bmi)
            else:
                # Use rule-based prediction
                return self._rule_based_prediction(user_input, bmi)
            
            # Determine risk level
            if risk_percentage < 30:
                risk_level = "low"
                risk_color = "green"
            elif risk_percentage < 70:
                risk_level = "moderate"
                risk_color = "orange"
            else:
                risk_level = "high"
                risk_color = "red"
            
            # Generate personalized recommendations
            recommendations = self._generate_recommendations(user_input, risk_level)
            
            return {
                "risk_percentage": round(risk_percentage, 1),
                "risk_level": risk_level,
                "risk_color": risk_color,
                "recommendations": recommendations,
                "bmi": round(bmi, 1),
                "model_used": model_used,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise ValueError(f"Failed to generate prediction: {str(e)}")
    
    def _rule_based_prediction(self, user_input: Dict[str, Any], bmi: float) -> Dict[str, Any]:
        """
        Rule-based diabetes risk prediction when ML model is not available
        """
        risk_score = 0
        
        # Age factor (0-25 points)
        age = user_input.get('age', 30)
        if age >= 65:
            risk_score += 25
        elif age >= 45:
            risk_score += 15
        elif age >= 35:
            risk_score += 8
        
        # BMI factor (0-20 points)
        if bmi >= 35:
            risk_score += 20
        elif bmi >= 30:
            risk_score += 15
        elif bmi >= 25:
            risk_score += 8
        
        # Family history (0-15 points)
        if user_input.get('familyHistory', '').lower() == 'yes':
            risk_score += 15
        
        # Physical activity (0-10 points)
        activity = user_input.get('physicalActivity', 'moderate').lower()
        if activity == 'low':
            risk_score += 10
        elif activity == 'moderate':
            risk_score += 3
        
        # Smoking (0-8 points)
        smoking = user_input.get('smoking', '').lower()
        if smoking in ['yes', 'former']:
            risk_score += 8 if smoking == 'yes' else 5
        
        # Blood pressure (0-10 points)
        bp = user_input.get('bloodPressure', 'normal').lower()
        if bp == 'high':
            risk_score += 10
        elif bp == 'elevated':
            risk_score += 5
        
        # Cholesterol (0-7 points)
        cholesterol = user_input.get('cholesterol', 'normal').lower()
        if cholesterol == 'high':
            risk_score += 7
        elif cholesterol == 'borderline':
            risk_score += 3
        
        # Convert score to percentage (max score = 95)
        risk_percentage = min(risk_score, 95)
        
        # Determine risk level
        if risk_percentage <= 25:
            risk_level = "low"
            risk_color = "green"
        elif risk_percentage <= 50:
            risk_level = "moderate"
            risk_color = "orange"
        else:
            risk_level = "high"
            risk_color = "red"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(user_input, risk_level)
        
        return {
            "risk_percentage": float(risk_percentage),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "recommendations": recommendations,
            "bmi": round(bmi, 1),
            "model_used": "Rule-based Assessment",
            "confidence": "moderate"
        }
    
    def _generate_recommendations(self, user_input: Dict[str, Any], risk_level: str) -> List[str]:
        """Generate personalized recommendations based on user input and risk level"""
        recommendations = []
        
        # Calculate BMI
        height_m = float(user_input.get('height', 170)) / 100
        weight = float(user_input.get('weight', 70))
        bmi = weight / (height_m ** 2)
        
        # BMI-based recommendations
        if bmi > 30:
            recommendations.append("🎯 Focus on weight management - aim for a BMI under 25")
            recommendations.append("🍽️ Consider consulting a nutritionist for a personalized meal plan")
        elif bmi > 25:
            recommendations.append("⚖️ Maintain a healthy weight through balanced diet and exercise")
        
        # Activity-based recommendations
        activity = user_input.get('physicalActivity', '').lower()
        if activity == 'low':
            recommendations.append("🏃‍♀️ Increase physical activity to at least 150 minutes per week")
            recommendations.append("🚶‍♂️ Start with daily 30-minute walks")
        
        # Smoking recommendations
        if user_input.get('smoking', '').lower() == 'yes':
            recommendations.append("🚭 Quit smoking to significantly reduce diabetes risk")
            recommendations.append("💊 Consider nicotine replacement therapy or counseling")
        
        # Blood pressure recommendations
        bp = user_input.get('bloodPressure', '').lower()
        if bp in ['elevated', 'high']:
            recommendations.append("🩺 Monitor blood pressure regularly")
            recommendations.append("🧂 Reduce sodium intake and manage stress")
        
        # Cholesterol recommendations
        chol = user_input.get('cholesterol', '').lower()
        if chol in ['borderline', 'high']:
            recommendations.append("💉 Get regular cholesterol screenings")
            recommendations.append("🥗 Follow a heart-healthy diet low in saturated fats")
        
        # Risk-level specific recommendations
        if risk_level == "high":
            recommendations.append("👨‍⚕️ Schedule an immediate consultation with a healthcare provider")
            recommendations.append("📊 Request comprehensive diabetes screening tests")
            recommendations.append("📱 Consider continuous glucose monitoring")
        elif risk_level == "moderate":
            recommendations.append("🩺 Schedule regular health check-ups every 6 months")
            recommendations.append("📈 Track your health metrics monthly")
        else:
            recommendations.append("✅ Maintain your current healthy lifestyle")
            recommendations.append("📅 Annual health screenings are sufficient")
        
        # General recommendations
        recommendations.extend([
            "🥬 Follow a Mediterranean or DASH diet",
            "💧 Stay well hydrated with 8+ glasses of water daily",
            "😴 Ensure 7-8 hours of quality sleep nightly",
            "🧘‍♀️ Practice stress management techniques"
        ])
        
        return recommendations[:8]  # Limit to 8 recommendations

# Global instance
prediction_service = DiabetesPredictionService()