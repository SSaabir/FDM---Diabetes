import requests

# Quick Railway check
base_url = "https://fdm-diabetes-production.up.railway.app"

print("🚨 QUICK RAILWAY CHECK")
print("=" * 30)

# Test reload
try:
    print("🔄 Reloading scaler...")
    r = requests.post(f"{base_url}/api/reload-scaler", timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"   Status: {data.get('status')}")
        print(f"   Loaded: {data.get('scaler_loaded')}")
        print(f"   Features: {data.get('scaler_features')}")
    else:
        print(f"   Failed: {r.status_code}")
except Exception as e:
    print(f"   Error: {e}")

# Test exact same prediction
test_data = {
    "age": 38, "gender": "female", "height": 158, "weight": 75,
    "familyHistory": "unknown", "physicalActivity": "moderate", 
    "smoking": "never", "hypertension": "no", "heartDisease": "no",
    "sleepHours": 7, "dietPattern": "balanced", "alcoholIntake": "occasional",
    "medicationUse": "no", "gestationalHistory": "no", "hbA1c": 5.8, "bloodGlucose": 95
}

try:
    print("\n🧪 Testing prediction...")
    r = requests.post(f"{base_url}/api/predict-public", json=test_data, timeout=10)
    if r.status_code == 200:
        result = r.json()
        risk = result.get('risk_percentage', 0)
        print(f"   Risk: {risk}%")
        if risk == 100:
            print("🚨 STILL BROKEN!")
        else:
            print("✅ WORKING!")
    else:
        print(f"   Failed: {r.status_code}")
except Exception as e:
    print(f"   Error: {e}")