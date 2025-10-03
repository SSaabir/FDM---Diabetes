import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict, Tuple
import logging
import joblib
import json

logger = logging.getLogger(__name__)

class DiabetesPredictionService:
    def __init__(self):
        self.models_path = Path(__file__).parent.parent.parent / "models"
        self.model = None
        self.scaler = None
        self.feature_columns = None
        
        self.load_model()

    def load_model(self):
        """Load a simple diabetes prediction model"""
        try:
            # Try to load the basic RF model
            model_path = self.models_path / "diabetes_rf_tuned.pkl"
            
            if model_path.exists():
                self.model = joblib.load(model_path)
                logger.info(f"✅ Model loaded: {model_path}")
            else:
                logger.warning("⚠️  Model file not found, using fallback prediction")
                self.model = None
                
        except Exception as e:
            logger.error(f"❌ Error loading model: {str(e)}")
            self.model = None

    def preprocess_input(self, user_input: Dict[str, Any]) -> Dict[str, float]:
        """Simple preprocessing of user input"""
        try:
            # Extract basic inputs
            age = float(user_input.get('age', 35))
            height = float(user_input.get('height', 170))
            weight = float(user_input.get('weight', 70))
            
            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)
            
            # Extract categorical inputs
            gender = user_input.get('gender', 'male').lower()
            smoking_history = user_input.get('smoking_history', 'never').lower()
            hypertension = 1 if user_input.get('hypertension', False) else 0
            heart_disease = 1 if user_input.get('heart_disease', False) else 0
            family_history = 1 if user_input.get('family_history', False) else 0
            
            # Create feature dictionary
            features = {
                'age': age,
                'bmi': bmi,
                'gender': 1 if gender == 'male' else 0,
                'smoking_history': self._encode_smoking(smoking_history),
                'hypertension': hypertension,
                'heart_disease': heart_disease,
                'family_history': family_history,
                'physical_activity': float(user_input.get('physical_activity', 2.5)),
                'diet_pattern': self._encode_diet(user_input.get('diet_pattern', 'balanced')),
                'sleep_hours': float(user_input.get('sleep_hours', 7.5)),
                'alcohol_intake': self._encode_alcohol(user_input.get('alcohol_intake', 'none')),
                'stress_level': self._encode_stress(user_input.get('stress_level', 'moderate'))
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise ValueError(f"Invalid input data: {str(e)}")

    def _encode_smoking(self, smoking_history: str) -> int:
        smoking_map = {
            'never': 0,
            'former': 1,
            'current': 2,
            'not current': 1,
            'no info': 0
        }
        return smoking_map.get(smoking_history.lower(), 0)

    def _encode_diet(self, diet_pattern: str) -> int:
        diet_map = {
            'balanced': 0,
            'low_carb': 1,
            'high_protein': 2,
            'vegetarian': 3,
            'processed': 4
        }
        return diet_map.get(diet_pattern.lower(), 0)

    def _encode_alcohol(self, alcohol_intake: str) -> int:
        alcohol_map = {
            'none': 0,
            'occasional': 1,
            'moderate': 2,
            'frequent': 3
        }
        return alcohol_map.get(alcohol_intake.lower(), 0)

    def _encode_stress(self, stress_level: str) -> int:
        stress_map = {
            'low': 0,
            'moderate': 1,
            'high': 2
        }
        return stress_map.get(stress_level.lower(), 1)

    def predict_diabetes_risk(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Predict diabetes risk from user input"""
        try:
            # Preprocess input
            features = self.preprocess_input(user_input)
            
            if self.model is not None:
                # Use ML model for prediction
                feature_df = pd.DataFrame([features])
                risk_probability = self.model.predict_proba(feature_df)[0][1]
                model_used = "Random Forest Model"
            else:
                # Use simple risk calculator as fallback
                risk_probability = self._calculate_risk_fallback(features)
                model_used = "Risk Calculator (Fallback)"
            
            # Determine risk level
            if risk_probability < 0.3:
                risk_level = "Low"
                recommendations = [
                    "Maintain a healthy lifestyle",
                    "Regular exercise and balanced diet",
                    "Annual health checkups"
                ]
            elif risk_probability < 0.6:
                risk_level = "Moderate"
                recommendations = [
                    "Increase physical activity",
                    "Monitor blood glucose levels",
                    "Consider dietary consultation"
                ]
            else:
                risk_level = "High"
                recommendations = [
                    "Consult healthcare provider immediately",
                    "Regular blood glucose monitoring",
                    "Lifestyle intervention program"
                ]

            return {
                "risk_probability": round(risk_probability, 4),
                "risk_level": risk_level,
                "recommendations": recommendations,
                "model_used": model_used,
                "bmi": round(features['bmi'], 2)
            }

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                "error": f"Prediction failed: {str(e)}",
                "risk_probability": 0.0,
                "risk_level": "Unknown",
                "recommendations": ["Please check your input and try again"],
                "model_used": "Error",
                "bmi": 0.0
            }

    def _calculate_risk_fallback(self, features: Dict[str, float]) -> float:
        """Simple risk calculation fallback"""
        risk_score = 0.0
        
        # Age factor
        if features['age'] > 45:
            risk_score += 0.2
        elif features['age'] > 35:
            risk_score += 0.1
            
        # BMI factor
        bmi = features['bmi']
        if bmi > 30:
            risk_score += 0.3
        elif bmi > 25:
            risk_score += 0.15
            
        # Medical history
        if features['hypertension']:
            risk_score += 0.2
        if features['heart_disease']:
            risk_score += 0.15
        if features['family_history']:
            risk_score += 0.25
            
        # Lifestyle factors
        if features['smoking_history'] == 2:  # current smoker
            risk_score += 0.1
        if features['physical_activity'] < 2:
            risk_score += 0.1
        if features['stress_level'] == 2:  # high stress
            risk_score += 0.05
            
        return min(risk_score, 0.95)  # Cap at 95%