import requests
import json

def emergency_railway_check():
    """Emergency check of Railway server"""
    
    base_url = "https://fdm-diabetes-production.up.railway.app"
    
    print("🚨 EMERGENCY RAILWAY CHECK")
    print("=" * 40)
    
    # Check filesystem
    try:
        print("📁 Checking filesystem...")
        response = requests.get(f"{base_url}/api/diagnose-files", timeout=10)
        if response.status_code == 200:
            data = response.json()
            scaler_exists = data.get('scaler_exists', False)
            models_contents = data.get('models_contents', [])
            print(f"   Scaler exists: {scaler_exists}")
            print(f"   Models contents: {models_contents}")
        else:
            print(f"   Filesystem check failed: {response.status_code}")
    except Exception as e:
        print(f"   Filesystem error: {e}")
    
    # Force reload scaler
    try:
        print("\n🔄 Force reloading scaler...")
        response = requests.post(f"{base_url}/api/reload-scaler", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Reload status: {data.get('status')}")
            print(f"   Scaler loaded: {data.get('scaler_loaded')}")
            print(f"   Features: {data.get('scaler_features')}")
        else:
            print(f"   Reload failed: {response.status_code}")
    except Exception as e:
        print(f"   Reload error: {e}")
    
    # Test with the exact same profile that's failing
    try:
        print("\n🧪 Testing exact failing profile...")
        test_data = {
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
        
        response = requests.post(f"{base_url}/api/predict-public", json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            risk = result.get('risk_percentage', 0)
            print(f"   Risk prediction: {risk}%")
            
            if risk == 100:
                print("🚨 CONFIRMED: Back to 100% - scaler issue returned!")
            else:
                print(f"✅ Working: {risk}% (reasonable)")
        else:
            print(f"   Prediction failed: {response.status_code}")
            
    except Exception as e:
        print(f"   Test error: {e}")

if __name__ == "__main__":
    emergency_railway_check()