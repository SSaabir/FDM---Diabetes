import joblib
import json
import numpy as np

# Test input data
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

print("🔍 Comparing compressed vs original models:")
print(f"Input: {user_input}")
print("\n" + "="*60)

try:
    # Load feature lists
    with open('models/general_model_features.json', 'r') as f:
        general_features_data = json.load(f)
        general_features = general_features_data['features']
    
    print(f"Features to use: {len(general_features)}")
    
    # Calculate BMI and basic preprocessing
    height_m = user_input['height'] / 100
    bmi = user_input['weight'] / (height_m ** 2)
    
    # Create feature vector
    features_dict = {}
    for feature in general_features:
        features_dict[feature] = 0.0
    
    # Normalize age and BMI (using estimated training stats)
    age_normalized = (user_input['age'] - 41.89) / 22.52
    bmi_normalized = (bmi - 27.32) / 6.64
    features_dict['age'] = age_normalized
    features_dict['bmi'] = bmi_normalized
    
    # Estimate HbA1c and glucose
    base_hba1c = 5.2
    if user_input['age'] > 45: base_hba1c += 0.2
    if bmi > 30: base_hba1c += 0.4
    if user_input['familyHistory'] == 'yes': base_hba1c += 0.3
    if user_input['bloodPressure'] == 'high': base_hba1c += 0.2
    if user_input['cholesterol'] == 'high': base_hba1c += 0.2
    if user_input['smoking'] == 'yes': base_hba1c += 0.1
    hba1c_val = min(base_hba1c, 8.0)
    
    base_glucose = 90
    if user_input['age'] > 45: base_glucose += 5
    if bmi > 30: base_glucose += 15
    if user_input['familyHistory'] == 'yes': base_glucose += 10
    if user_input['bloodPressure'] == 'high': base_glucose += 8
    if user_input['cholesterol'] == 'high': base_glucose += 5
    glucose_val = min(base_glucose, 200)
    
    hba1c_normalized = (hba1c_val - 5.53) / 1.07
    glucose_normalized = (glucose_val - 138.06) / 40.71
    features_dict['hbA1c_level'] = hba1c_normalized
    features_dict['blood_glucose_level'] = glucose_normalized
    
    # Gender, smoking, BMI categories, age groups, etc.
    features_dict['gender_Male'] = 1.0
    features_dict['smoking_history_current'] = 1.0
    features_dict['bmi_category_Obese'] = 1.0
    features_dict['age_group_Senior'] = 1.0
    features_dict['bmi_risk_level_obese_2'] = 1.0
    features_dict['age_diabetes_risk_high_risk'] = 1.0
    
    # Convert to array
    feature_array = np.array([[features_dict[feature] for feature in general_features]])
    
    print(f"\n📊 Preprocessing results:")
    print(f"BMI: {bmi:.2f}")
    print(f"Estimated HbA1c: {hba1c_val:.2f} (normalized: {hba1c_normalized:.3f})")
    print(f"Estimated glucose: {glucose_val:.2f} (normalized: {glucose_normalized:.3f})")
    
    # Test compressed model
    print(f"\n🗜️ COMPRESSED MODEL:")
    compressed_model = joblib.load('models/diabetes_general_model_compressed_lvl3.pkl')
    compressed_proba = compressed_model.predict_proba(feature_array)[0]
    print(f"Diabetes probability: {compressed_proba[1]:.6f} ({compressed_proba[1]*100:.2f}%)")
    
    # Test original model
    print(f"\n📦 ORIGINAL MODEL:")
    original_model = joblib.load('models/diabetes_general_model.pkl')
    original_proba = original_model.predict_proba(feature_array)[0]
    print(f"Diabetes probability: {original_proba[1]:.6f} ({original_proba[1]*100:.2f}%)")
    
    # Compare
    diff = abs(compressed_proba[1] - original_proba[1]) * 100
    print(f"\n🔄 COMPARISON:")
    print(f"Difference: {diff:.4f} percentage points")
    print(f"Compression accuracy: {100 - diff:.4f}%")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()