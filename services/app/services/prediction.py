import numpy as np
from pathlib import Path
from typing import Any, Dict
import logging
import joblib
import json

logger = logging.getLogger(__name__)

class DiabetesPredictionService:
    def __init__(self):
        self.models_path = Path(__file__).parent.parent.parent / "models"
        self.processed_data_path = Path(__file__).parent.parent.parent / "data" / "processed_enhanced"
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
        Preprocess user input for Random Forest model with all 29 features
        """
        try:
            # Sanitize inputs
            age = self._sanitize_input('age', user_input.get('age', 30))
            height = self._sanitize_input('height', user_input.get('height', 170))
            weight = self._sanitize_input('weight', user_input.get('weight', 70))
            bmi = weight / ((height / 100) ** 2)
            gender = self._sanitize_input('gender', user_input.get('gender', ''))
            smoking = self._sanitize_input('smoking', user_input.get('smoking', 'never'))
            
            # Estimate HbA1c and glucose based on risk factors if not provided
            hba1c_val = user_input.get('hbA1c_level')
            glucose_val = user_input.get('blood_glucose_level')
            
            if hba1c_val is None:
                # Estimate HbA1c based on risk factors
                base_hba1c = 5.2  # Normal baseline
                if age > 45: base_hba1c += 0.2
                if bmi > 30: base_hba1c += 0.4
                elif bmi > 25: base_hba1c += 0.2
                if user_input.get('familyHistory') == 'yes': base_hba1c += 0.3
                if user_input.get('physicalActivity') == 'low': base_hba1c += 0.3
                if user_input.get('bloodPressure') == 'high': base_hba1c += 0.2
                if user_input.get('cholesterol') == 'high': base_hba1c += 0.2
                if smoking in ['yes', 'current']: base_hba1c += 0.1
                hba1c_val = min(base_hba1c, 8.0)  # Cap at reasonable max
                
            if glucose_val is None:
                # Estimate glucose based on risk factors
                base_glucose = 90  # Normal baseline
                if age > 45: base_glucose += 5
                if bmi > 30: base_glucose += 15
                elif bmi > 25: base_glucose += 8
                if user_input.get('familyHistory') == 'yes': base_glucose += 10
                if user_input.get('physicalActivity') == 'low': base_glucose += 10
                if user_input.get('bloodPressure') == 'high': base_glucose += 8
                if user_input.get('cholesterol') == 'high': base_glucose += 5
                glucose_val = min(base_glucose, 180)  # Cap at reasonable max

            hba1c_val = self._sanitize_input('hbA1c_level', hba1c_val)
            glucose_val = self._sanitize_input('blood_glucose_level', glucose_val)

            # Initialize feature dictionary with all 29 features
            features_dict = {col: 0.0 for col in self.feature_columns}

            # Basic features with proper scaling
            features_dict['age'] = (age - 41.885856) / 22.51683987161702
            features_dict['bmi'] = (bmi - 27.320767099999994) / 6.636783416648368
            features_dict['hbA1c_level'] = (hba1c_val - 6.0) / 1.5
            features_dict['blood_glucose_level'] = (glucose_val - 120) / 40

            # Gender encoding
            features_dict['gender_Female'] = 1.0 if gender == 'female' else 0.0
            features_dict['gender_Male'] = 1.0 if gender == 'male' else 0.0

            # Smoking history - map form values to model features
            if smoking in ['no', 'never']:
                features_dict['smoking_history_never'] = 1.0
            elif smoking in ['yes', 'current']:
                features_dict['smoking_history_current'] = 1.0
            elif smoking == 'former':
                features_dict['smoking_history_former'] = 1.0
            else:
                features_dict['smoking_history_never'] = 1.0  # default

            # BMI categories
            if bmi < 18.5:
                features_dict['bmi_category_Underweight'] = 1.0
                features_dict['bmi_risk_level_underweight'] = 1.0
            elif bmi < 25:
                features_dict['bmi_category_Normal'] = 1.0
                features_dict['bmi_risk_level_normal'] = 1.0
            elif bmi < 30:
                features_dict['bmi_category_Overweight'] = 1.0
                features_dict['bmi_risk_level_overweight'] = 1.0
            elif bmi < 35:
                features_dict['bmi_category_Obese'] = 1.0
                features_dict['bmi_risk_level_obese_1'] = 1.0
            else:
                features_dict['bmi_category_Obese'] = 1.0
                features_dict['bmi_risk_level_obese_2'] = 1.0

            # Age groups
            if age < 18:
                features_dict['age_group_Child'] = 1.0
                features_dict['age_diabetes_risk_low_risk'] = 1.0
            elif age < 45:
                features_dict['age_group_Adult'] = 1.0
                features_dict['age_diabetes_risk_low_risk'] = 1.0
            elif age < 65:
                features_dict['age_group_Middle-aged'] = 1.0
                features_dict['age_diabetes_risk_moderate_risk'] = 1.0
            else:
                features_dict['age_group_Senior'] = 1.0
                features_dict['age_diabetes_risk_high_risk'] = 1.0

            # Convert to numpy array in correct order
            feature_array = np.array([features_dict[col] for col in self.feature_columns]).reshape(1, -1)
            logger.info(f"✅ Generated all {len(self.feature_columns)} features for Random Forest model")
            logger.info(f"🔬 Estimated HbA1c: {hba1c_val:.1f}, Glucose: {glucose_val:.0f}")
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
        Generate comprehensive health recommendations based on risk level and user profile
        """
        recommendations = []
        age = float(user_input.get('age', 30))
        height = float(user_input.get('height', 170))
        weight = float(user_input.get('weight', 70))
        bmi = weight / ((height / 100) ** 2)
        
        if risk_level.lower().startswith("high"):
            recommendations.extend([
                "🏥 Consult with a healthcare provider within 2 weeks",
                "🍽️ Follow a strict low-glycemic meal plan",
                "💊 Discuss preventive medications (metformin) with doctor",
                "🩸 Get comprehensive blood work (HbA1c, fasting glucose)",
                "📋 Consider referral to endocrinologist"
            ])
            if bmi > 30:
                recommendations.append("⚖️ Work with nutritionist for weight management")
            if user_input.get('physicalActivity') == 'low':
                recommendations.append("🏋️‍♂️ Start supervised exercise program")
                
        elif risk_level.lower().startswith("moderate"):
            recommendations.extend([
                "🍎 Follow diabetes prevention diet (low processed foods)",
                "🏋️‍♂️ Increase physical activity to 200+ min/week",
                "🩺 Schedule health check-ups every 6 months",
                "📊 Monitor blood pressure and cholesterol regularly"
            ])
            if bmi > 25:
                recommendations.append("⚖️ Work towards achieving ideal body weight")
            if user_input.get('smoking') in ['yes', 'current']:
                recommendations.append("🚭 Consider smoking cessation programs")
                
        else:  # Low risk
            recommendations.extend([
                "🥗 Maintain a balanced, nutrient-rich diet",
                "🏃‍♂️ Continue regular physical activity (150+ min/week)",
                "📅 Schedule annual health screenings",
                "💧 Stay well-hydrated and limit sugary drinks"
            ])
            if age > 40:
                recommendations.append("🧪 Annual diabetes screening recommended")
                
        return recommendations

    # -------------------------------
    # ✅ Load ML models
    # -------------------------------
    def load_models(self):
        """
        Load ML models, feature columns, and scaler from disk
        """
        try:
            # Load Random Forest model
            rf_model_path = self.models_path / "diabetes_rf_tuned.pkl"
            if rf_model_path.exists():
                self.rf_model = joblib.load(rf_model_path)
                logger.info("✅ Random Forest model loaded successfully")
            else:
                logger.warning("❌ Random Forest model not found")
                
            # Load feature columns
            feature_cols_path = self.models_path / "feature_columns.json"
            if feature_cols_path.exists():
                with open(feature_cols_path, 'r') as f:
                    feature_data = json.load(f)
                    # Handle both list and dict formats
                    if isinstance(feature_data, list):
                        self.feature_columns = feature_data
                    elif isinstance(feature_data, dict):
                        self.feature_columns = feature_data.get('features', list(feature_data.keys()))
                    else:
                        raise ValueError("Unexpected feature columns format")
                logger.info(f"✅ Feature columns loaded: {len(self.feature_columns)} features")
            else:
                logger.warning("❌ Feature columns file not found, using default")
                self.feature_columns = ["age", "bmi", "hbA1c_level", "blood_glucose_level",
                                      "gender_Female", "gender_Male", 
                                      "smoking_history_never", "smoking_history_current", "smoking_history_former"]
            
            # Load the enhanced preprocessing scaler
            scaler_path = self.processed_data_path / "feature_scaler.pkl"
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
                logger.info("✅ Enhanced preprocessing scaler loaded successfully")
            else:
                logger.warning("❌ Enhanced preprocessing scaler not found, will use manual scaling")
                self.scaler = None
                
        except Exception as e:
            logger.error(f"❌ Failed to load models: {str(e)}")
            # Set fallback values
            self.rf_model = None
            self.feature_columns = ["age", "bmi", "hbA1c_level", "blood_glucose_level",
                                  "gender_Female", "gender_Male",
                                  "smoking_history_never", "smoking_history_current", "smoking_history_former"]
            self.scaler = None


# Create a global instance of the prediction service
prediction_service = DiabetesPredictionService()
