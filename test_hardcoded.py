import sys
sys.path.append('services/app')

def test_hardcoded_scaler():
    """Test the hardcoded scaler"""
    
    print("🧪 TESTING HARDCODED SCALER")
    print("=" * 30)
    
    try:
        from services.prediction import DiabetesPredictionService
        
        service = DiabetesPredictionService()
        
        # Test prediction with the exact profile that was failing
        test_input = {
            "age": 38,
            "gender": "female",
            "height": 158,
            "weight": 75,
            "familyHistory": "unknown",
            "physicalActivity": "moderate",
            "smoking": "never",
            "hypertension": "no",
            "heartDisease": "no",
            "sleepHours": 7,
            "dietPattern": "balanced",
            "alcoholIntake": "occasional",
            "medicationUse": "no",
            "gestationalHistory": "no",
            "hbA1c": 5.8,
            "bloodGlucose": 95
        }
        
        result = service.predict_diabetes_risk(test_input)
        risk = result.get('risk_percentage', 0)
        
        print(f"✅ Prediction successful!")
        print(f"   Risk: {risk}%")
        print(f"   Model: {result.get('model_used', 'unknown')}")
        
        if risk < 50:
            print(f"🎉 SUCCESS! Hardcoded scaler working - realistic risk!")
        else:
            print(f"❌ Still high risk: {risk}%")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hardcoded_scaler()