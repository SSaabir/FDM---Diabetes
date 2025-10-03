import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.prediction import DiabetesPredictionService

# Test input - 73-year-old with multiple risk factors
user_input = {
    "age": 73,
    "gender": "male", 
    "height": 160,
    "weight": 90,
    "familyHistory": "yes",
    "physicalActivity": "high",
    "smoking": "yes", 
    "bloodPressure": "high",
    "cholesterol": "high",
    "gestationalHistory": False
}

print("🔍 Testing improved risk assessment:")
print(f"Input: 73-year-old male with multiple risk factors")
print("\n" + "="*60)

try:
    # Initialize prediction service
    service = DiabetesPredictionService()
    
    # Get prediction with new improvements
    result = service.predict_diabetes_risk(user_input)
    
    print(f"📊 IMPROVED RESULTS:")
    print(f"Risk percentage: {result['risk_percentage']}%")
    print(f"Risk level: {result['risk_level']}")
    print(f"Risk color: {result['risk_color']}")
    print(f"Model used: {result['model_used']}")
    print(f"Confidence: {result['confidence']}")
    
    print(f"\n🆚 COMPARISON:")
    print(f"OLD SYSTEM: 23.8% (low risk, green)")
    print(f"NEW SYSTEM: {result['risk_percentage']}% ({result['risk_level']} risk, {result['risk_color']})")
    
    # Calculate BMI for context
    height_m = user_input['height'] / 100
    bmi = user_input['weight'] / (height_m ** 2)
    print(f"\n📋 RISK FACTORS:")
    print(f"• Age: {user_input['age']} (senior)")
    print(f"• BMI: {bmi:.1f} (obese class 2)")
    print(f"• Blood pressure: {user_input['bloodPressure']}")
    print(f"• Cholesterol: {user_input['cholesterol']}")
    print(f"• Family history: {user_input['familyHistory']}")
    print(f"• Smoking: {user_input['smoking']}")
    print(f"• Physical activity: {user_input['physicalActivity']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()