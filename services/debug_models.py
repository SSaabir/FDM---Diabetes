"""
Debug script to test model loading
"""

import sys
import os
from pathlib import Path
import joblib
import json

# Add the services directory to the path
services_path = Path(__file__).parent
sys.path.append(str(services_path))

def test_model_loading():
    """Test loading all models and features"""
    
    models_path = Path(__file__).parent / "models"
    print(f"Models path: {models_path}")
    print(f"Models path exists: {models_path.exists()}")
    
    print("\n📁 Checking Model Files:")
    print("=" * 40)
    
    # Check compressed model
    compressed_path = models_path / "diabetes_general_model_compressed_lvl3.pkl"
    print(f"Compressed model exists: {compressed_path.exists()}")
    if compressed_path.exists():
        try:
            model = joblib.load(compressed_path)
            print(f"✅ Compressed model loaded: {type(model)}")
        except Exception as e:
            print(f"❌ Failed to load compressed model: {e}")
    
    # Check original model
    original_path = models_path / "diabetes_general_model.pkl"
    print(f"Original model exists: {original_path.exists()}")
    if original_path.exists():
        try:
            model = joblib.load(original_path)
            print(f"✅ Original model loaded: {type(model)}")
        except Exception as e:
            print(f"❌ Failed to load original model: {e}")
    
    # Check women's model
    women_path = models_path / "diabetes_women_model.pkl"
    print(f"Women's model exists: {women_path.exists()}")
    if women_path.exists():
        try:
            model = joblib.load(women_path)
            print(f"✅ Women's model loaded: {type(model)}")
        except Exception as e:
            print(f"❌ Failed to load women's model: {e}")
    
    # Check feature files
    print(f"\n📄 Checking Feature Files:")
    print("=" * 30)
    
    general_features_path = models_path / "general_model_features.json"
    print(f"General features exists: {general_features_path.exists()}")
    if general_features_path.exists():
        try:
            with open(general_features_path, 'r') as f:
                features = json.load(f)
            print(f"✅ General features loaded: {len(features.get('features', []))} features")
        except Exception as e:
            print(f"❌ Failed to load general features: {e}")
    
    women_features_path = models_path / "women_model_features.json"
    print(f"Women features exists: {women_features_path.exists()}")
    if women_features_path.exists():
        try:
            with open(women_features_path, 'r') as f:
                features = json.load(f)
            print(f"✅ Women features loaded: {len(features.get('features', []))} features")
        except Exception as e:
            print(f"❌ Failed to load women features: {e}")

def test_prediction_service():
    """Test the actual prediction service"""
    
    print(f"\n🧪 Testing Prediction Service:")
    print("=" * 35)
    
    try:
        from app.services.prediction import DiabetesPredictionService
        
        service = DiabetesPredictionService()
        
        print(f"General model loaded: {service.general_model is not None}")
        print(f"Women model loaded: {service.women_model is not None}")
        print(f"Legacy model loaded: {service.rf_model is not None}")
        
        if service.general_model:
            print(f"General model type: {type(service.general_model)}")
        if service.women_model:
            print(f"Women model type: {type(service.women_model)}")
        if service.rf_model:
            print(f"Legacy model type: {type(service.rf_model)}")
            
        # Test prediction
        test_data = {
            'age': 45,
            'gender': 'male',
            'height': 175,
            'weight': 80,
            'hypertension': 0,
            'heart_disease': 0,
            'smoking_history': 'never',
            'hbA1c_level': 6.2,
            'blood_glucose_level': 140
        }
        
        result = service.predict_diabetes_risk(test_data)
        print(f"\n📊 Prediction Result:")
        print(f"   Model used: {result.get('model_used', 'Unknown')}")
        print(f"   Risk level: {result.get('risk_level', 'Unknown')}")
        print(f"   Confidence: {result.get('confidence', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Prediction service test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Model Loading Debug Script")
    print("=" * 50)
    
    test_model_loading()
    test_prediction_service()