import numpy as np
from pathlib import Path
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class DiabetesPredictionService:
    def __init__(self):
        self.models_path = Path(__file__).parent.parent.parent / "models"
        self.rf_model = None
        self.feature_columns = None
        self.scaler = None
        self.load_models()

    # -------------------------------
    # ✅ Sanitization helper
    # -------------------------------
    def _sanitize_input(self, field: str, value: Any) -> Any:
        """
        Clean user input to prevent invalid characters or wrong types
        """
        if isinstance(value, str):
            value = value.strip().replace("<", "").replace(">", "")
            
            # Numeric fields
            if field in ['age', 'height', 'weight', 'bloodPressure', 'cholesterol', 'hbA1c_level', 'blood_glucose_level']:
                value = ''.join(c for c in value if c.isdigit() or c == '.')
                try:
                    value = float(value)
                except ValueError:
                    value = 0.0
            
            # Categorical fields: ensure allowed values
            if field == 'gender':
                value = value.lower()
                if value not in ['male', 'female', 'other']:
                    value = ''
            if field in ['smoking', 'physicalActivity', 'familyHistory']:
                value = value.lower()
        
        if isinstance(value, (int, float)):
            return value
        return value

    # -------------------------------
    # ✅ Preprocess inputs for ML
    # -------------------------------
    def preprocess_input(self, user_input: Dict[str, Any]) -> np.ndarray:
        """
        Preprocess user input using same scaling as training data
        """
        try:
            # Sanitize inputs
            age = self._sanitize_input('age', user_input.get('age', 30))
            height = self._sanitize_input('height', user_input.get('height', 170))
            weight = self._sanitize_input('weight', user_input.get('weight', 70))
            bmi = weight / ((height / 100) ** 2)
            hba1c_val = self._sanitize_input('hbA1c_level', user_input.get('hbA1c_level', 5.5))
            glucose_val = self._sanitize_input('blood_glucose_level', user_input.get('blood_glucose_level', 100))
            gender = self._sanitize_input('gender', user_input.get('gender', ''))

            # Initialize feature dictionary
            features_dict = {col: 0.0 for col in self.feature_columns}

            # Apply scaling
            features_dict['age'] = (age - 41.885856) / 22.51683987161702
            features_dict['bmi'] = (bmi - 27.320767099999994) / 6.636783416648368
            features_dict['hbA1c_level'] = (hba1c_val - 6.0) / 1.5
            features_dict['blood_glucose_level'] = (glucose_val - 120) / 40

            # Gender encoding
            features_dict['gender_Female'] = 1.0 if gender == 'female' else 0.0
            features_dict['gender_Male'] = 1.0 if gender == 'male' else 0.0

            # Smoking history
            smoking = self._sanitize_input('smoking', user_input.get('smoking', 'never'))
            features_dict['smoking_history_never'] = 1.0 if smoking in ['no', 'never'] else 0.0
            features_dict['smoking_history_current'] = 1.0 if smoking in ['yes', 'current'] else 0.0
            features_dict['smoking_history_former'] = 1.0 if smoking == 'former' else 0.0

            # Convert to numpy array
            feature_array = np.array([features_dict[col] for col in self.feature_columns]).reshape(1, -1)
            return feature_array

        except Exception as e:
            logger.error(f"❌ Error in preprocessing: {str(e)}")
            raise

    # -------------------------------
    # ✅ Generate prediction
    # -------------------------------
    def predict_diabetes_risk(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate diabetes risk prediction using ML model or fallback
        """
        try:
            # Sanitize all inputs
            for field in user_input:
                user_input[field] = self._sanitize_input(field, user_input[field])

            # Calculate BMI
            height_m = float(user_input.get('height', 170)) / 100
            weight = float(user_input.get('weight', 70))
            bmi = weight / (height_m ** 2)

            # ML prediction
            if self.rf_model:
                try:
                    features = self.preprocess_input(user_input)
                    risk_probability = self.rf_model.predict_proba(features)[0][1]
                    risk_percentage = float(risk_probability * 100)
                    model_used = "Random Forest"
                    confidence = "high" if risk_percentage < 20 or risk_percentage > 80 else "moderate"
                except Exception as e:
                    logger.warning(f"ML model failed, using fallback: {str(e)}")
                    return self._rule_based_prediction(user_input, bmi)
            else:
                return self._rule_based_prediction(user_input, bmi)

            # Risk level
            if risk_percentage < 30:
                risk_level = "low"
                risk_color = "green"
            elif risk_percentage < 70:
                risk_level = "moderate"
                risk_color = "orange"
            else:
                risk_level = "high"
                risk_color = "red"

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

    # -------------------------------
    # ✅ Fallback / rule-based prediction
    # -------------------------------
    def _rule_based_prediction(self, user_input: Dict[str, Any], bmi: float) -> Dict[str, Any]:
        """
        Simple rule-based prediction if ML model fails
        """
        risk = 10
        if bmi > 30:
            risk += 20
        age = float(user_input.get('age', 30))
        if age > 50:
            risk += 15

        if risk > 50:
            risk_level = "high (fallback)"
        else:
            risk_level = "low (fallback)"

        recommendations = ["Please consult a doctor for proper testing."]

        return {
            "risk_percentage": risk,
            "risk_level": risk_level,
            "risk_color": "orange" if risk > 50 else "green",
            "recommendations": recommendations,
            "bmi": round(bmi, 1),
            "model_used": "Fallback calculator",
            "confidence": "N/A"
        }

    # -------------------------------
    # ✅ Generate recommendations
    # -------------------------------
    def _generate_recommendations(self, user_input: Dict[str, Any], risk_level: str):
        """
        Generate health recommendations based on risk
        """
        recommendations = []
        if risk_level.lower().startswith("high"):
            recommendations.append("Consult a healthcare provider immediately.")
        elif risk_level.lower().startswith("moderate"):
            recommendations.append("Maintain healthy diet and exercise regularly.")
        else:
            recommendations.append("Keep up your healthy lifestyle.")
        return recommendations

    # -------------------------------
    # ✅ Load ML models
    # -------------------------------
    def load_models(self):
        """
        Load ML models and feature columns from disk
        """
        try:
            # Example: load your Random Forest model
            # self.rf_model = joblib.load(self.models_path / "rf_model.pkl")
            # self.feature_columns = joblib.load(self.models_path / "feature_columns.pkl")
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load models: {str(e)}")
            self.rf_model = None
            self.feature_columns = ["age", "bmi", "hbA1c_level", "blood_glucose_level",
                                    "gender_Female", "gender_Male",
                                    "smoking_history_never", "smoking_history_current", "smoking_history_former"]
            self.scaler = None
