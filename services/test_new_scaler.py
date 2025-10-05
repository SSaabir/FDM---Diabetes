import pickle
import joblib
import numpy as np
import pandas as pd
import sys
import os

# Add the current directory to Python path
sys.path.append('.')
sys.path.append('app')

def test_prediction_with_new_scaler():
    """Test prediction with the newly generated scaler"""
    
    print("🔍 TESTING PREDICTION WITH NEW SCALER")
    print("=" * 50)
    
    # Test the scaler file directly
    scaler_path = 'data/processed_enhanced/feature_scaler.pkl'
    
    if os.path.exists(scaler_path):
        print(f"✅ Scaler file exists: {scaler_path}")
        
        try:
            scaler = joblib.load(scaler_path)
            
            print(f"✅ Scaler loaded successfully")
            print(f"   Type: {type(scaler)}")
            print(f"   Features: {scaler.n_features_in_}")
            print(f"   Means: {scaler.mean_}")
            print(f"   Scales: {scaler.scale_}")
            
            # Test with low-risk values
            test_data = np.array([[25, 22.04, 5.5, 95]])  # age, bmi, hbA1c, glucose
            print(f"\n🧪 Testing with low-risk data: {test_data[0]}")
            
            scaled_data = scaler.transform(test_data)
            print(f"   Scaled data: {scaled_data[0]}")
            
            # Check if values are reasonable (should be close to 0 for normal values)
            if np.all(np.abs(scaled_data[0]) < 5):  # Reasonable z-scores
                print(f"✅ Scaling looks correct (z-scores within reasonable range)")
            else:
                print(f"❌ Scaling looks wrong (z-scores too extreme)")
                
        except Exception as e:
            print(f"❌ Error loading scaler: {e}")
    else:
        print(f"❌ Scaler file not found: {scaler_path}")
    
    # Test with the prediction service
    print(f"\n🔍 Testing prediction service...")
    try:
        from services.prediction import DiabetesPredictionService
        
        service = DiabetesPredictionService()
        
        # Reload the scaler in the service
        service.load_scaler()
        
        # Test prediction with low-risk profile
        test_input = {
            "age": 25,
            "gender": "female", 
            "height": 165,
            "weight": 60,
            "familyHistory": "no",
            "gestationalHistory": "no", 
            "smoking": "never",
            "hbA1c": 5.5,
            "bloodGlucose": 95
        }
        
        result = service.predict_diabetes_risk(test_input)
        print(f"✅ Prediction service working")
        print(f"   Risk: {result.get('risk_percentage', 0)}%")
        print(f"   Model: {result.get('model_used', 'unknown')}")
        
        risk = result.get('risk_percentage', 0)
        if risk < 30:
            print(f"✅ LOCAL PREDICTION CORRECT - Low risk detected")
        else:
            print(f"❌ LOCAL PREDICTION WRONG - Still high risk: {risk}%")
            
    except Exception as e:
        print(f"❌ Error testing prediction service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction_with_new_scaler()