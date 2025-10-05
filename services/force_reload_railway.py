import requests
import json

def force_reload_railway_scaler():
    """Try to force reload the scaler on Railway"""
    
    base_url = "https://fdm-diabetes-production.up.railway.app"
    
    print("🔄 FORCING SCALER RELOAD ON RAILWAY")
    print("=" * 40)
    
    # Try to reload the scaler
    try:
        print("🌐 Attempting to reload scaler...")
        response = requests.post(f"{base_url}/api/reload-scaler", timeout=15)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reload successful: {data}")
            
            # Test prediction after reload
            print(f"\n🧪 Testing prediction after reload...")
            test_data = {
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
            
            pred_response = requests.post(f"{base_url}/api/predict-public", json=test_data, timeout=15)
            
            if pred_response.status_code == 200:
                pred_data = pred_response.json()
                risk = pred_data.get('risk_percentage', 0)
                print(f"   New prediction: {risk}% risk")
                
                if risk < 30:
                    print(f"🎉 SUCCESS! Scaler is now working on Railway!")
                else:
                    print(f"❌ Still returning high risk: {risk}%")
                    
                return risk
            else:
                print(f"❌ Prediction failed: {pred_response.status_code}")
                
        else:
            print(f"❌ Reload failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during reload: {e}")
    
    return None

def check_deployment_status():
    """Check if the deployment really updated"""
    
    base_url = "https://fdm-diabetes-production.up.railway.app"
    
    print("\n🔍 CHECKING DEPLOYMENT STATUS")
    print("=" * 40)
    
    # Check the health endpoint to see scaler status
    try:
        response = requests.get(f"{base_url}/api/health", timeout=15)
        print(f"Health endpoint status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Health endpoint error: {response.text}")
            print("This suggests scaler loading issue in the new deployment")
            
    except Exception as e:
        print(f"Health check error: {e}")

if __name__ == "__main__":
    check_deployment_status()
    risk = force_reload_railway_scaler()
    
    if risk is None or risk > 50:
        print("\n💡 NEXT STEPS:")
        print("1. Check Railway deployment logs for errors")
        print("2. Verify the scaler file was uploaded correctly")
        print("3. Try manual redeployment on Railway dashboard")
        print("4. Check if Railway has enough memory/resources")