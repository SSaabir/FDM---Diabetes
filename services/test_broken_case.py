import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.prediction import DiabetesPredictionService

# Test input that's showing 0.1% risk
user_input = {
    "age": 45,
    "gender": "male", 
    "height": 175,
    "weight": 87,
    "familyHistory": "yes",
    "physicalActivity": "low",
    "smoking": "yes", 
    "bloodPressure": "high",
    "cholesterol": "high",
    "gestationalHistory": False
}

print("🔍 Testing 45-year-old case locally:")
print(f"Input: {user_input}")
print("\n" + "="*60)

try:
    # Initialize prediction service
    service = DiabetesPredictionService()
    
    # Get prediction
    result = service.predict_diabetes_risk(user_input)
    
    print(f"📊 LOCAL RESULTS:")
    print(f"Risk percentage: {result['risk_percentage']}%")
    print(f"Risk level: {result['risk_level']}")
    print(f"Model used: {result['model_used']}")
    print(f"Confidence: {result['confidence']}")
    
    print(f"\n🆚 PRODUCTION COMPARISON:")
    print(f"PRODUCTION: 0.1% (low risk, green)")
    print(f"LOCAL: {result['risk_percentage']}% ({result['risk_level']} risk)")
    
    # Calculate BMI for context
    height_m = user_input['height'] / 100
    bmi = user_input['weight'] / (height_m ** 2)
    print(f"\n📋 RISK FACTORS:")
    print(f"• Age: {user_input['age']}")
    print(f"• BMI: {bmi:.1f}")
    print(f"• Blood pressure: {user_input['bloodPressure']}")
    print(f"• Cholesterol: {user_input['cholesterol']}")
    print(f"• Family history: {user_input['familyHistory']}")
    print(f"• Smoking: {user_input['smoking']}")
    print(f"• Physical activity: {user_input['physicalActivity']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()