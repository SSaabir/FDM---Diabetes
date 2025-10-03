import joblib
import json
import numpy as np

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

print("🔍 Testing compressed models directly:")
print(f"Input: 45-year-old with multiple risk factors")
print("\n" + "="*60)

try:
    # Load compressed model
    print("📂 Loading compressed model...")
    compressed_model = joblib.load('models/diabetes_general_model_compressed_lvl3.pkl')
    
    # Load feature lists
    with open('models/general_model_features.json', 'r') as f:
        general_features_data = json.load(f)
        general_features = general_features_data['features']
    
    print(f"✅ Compressed model loaded with {len(general_features)} features")
    
    # Calculate BMI and basic preprocessing
    height_m = user_input['height'] / 100
    bmi = user_input['weight'] / (height_m ** 2)
    
    # Create feature vector (simplified version)
    features_dict = {}
    for feature in general_features:
        features_dict[feature] = 0.0
    
    # Basic feature engineering
    age_normalized = (user_input['age'] - 41.89) / 22.52
    bmi_normalized = (bmi - 27.32) / 6.64
    features_dict['age'] = age_normalized
    features_dict['bmi'] = bmi_normalized
    
    # Estimate HbA1c and glucose
    base_hba1c = 5.2
    if user_input['age'] > 45: base_hba1c += 0.2
    if bmi > 30: base_hba1c += 0.4
    if user_input['familyHistory'] == 'yes': base_hba1c += 0.3
    if user_input['physicalActivity'] == 'low': base_hba1c += 0.3
    if user_input['bloodPressure'] == 'high': base_hba1c += 0.2
    if user_input['cholesterol'] == 'high': base_hba1c += 0.2
    if user_input['smoking'] == 'yes': base_hba1c += 0.1
    hba1c_val = min(base_hba1c, 8.0)
    
    base_glucose = 90
    if user_input['age'] > 45: base_glucose += 5
    if bmi > 30: base_glucose += 15
    if user_input['familyHistory'] == 'yes': base_glucose += 10
    if user_input['physicalActivity'] == 'low': base_glucose += 10
    if user_input['bloodPressure'] == 'high': base_glucose += 8
    if user_input['cholesterol'] == 'high': base_glucose += 5
    glucose_val = min(base_glucose, 200)
    
    hba1c_normalized = (hba1c_val - 5.53) / 1.07
    glucose_normalized = (glucose_val - 138.06) / 40.71
    features_dict['hbA1c_level'] = hba1c_normalized
    features_dict['blood_glucose_level'] = glucose_normalized
    
    # Gender, smoking, BMI categories, age groups
    features_dict['gender_Male'] = 1.0
    features_dict['smoking_history_current'] = 1.0
    
    if bmi >= 30:
        features_dict['bmi_category_Obese'] = 1.0
        features_dict['bmi_risk_level_obese_1'] = 1.0
    elif bmi >= 25:
        features_dict['bmi_category_Overweight'] = 1.0
        features_dict['bmi_risk_level_overweight'] = 1.0
    else:
        features_dict['bmi_category_Normal'] = 1.0
        features_dict['bmi_risk_level_normal'] = 1.0
        
    if user_input['age'] >= 60:
        features_dict['age_group_Senior'] = 1.0
    elif user_input['age'] >= 40:
        features_dict['age_group_Middle-aged'] = 1.0
    else:
        features_dict['age_group_Adult'] = 1.0
        
    if user_input['age'] >= 65:
        features_dict['age_diabetes_risk_high_risk'] = 1.0
    elif user_input['age'] >= 45:
        features_dict['age_diabetes_risk_moderate_risk'] = 1.0
    else:
        features_dict['age_diabetes_risk_low_risk'] = 1.0
    
    # Convert to array
    feature_array = np.array([[features_dict[feature] for feature in general_features]])
    
    print(f"\n📊 Feature processing:")
    print(f"BMI: {bmi:.2f} (normalized: {bmi_normalized:.3f})")
    print(f"Age: {user_input['age']} (normalized: {age_normalized:.3f})")
    print(f"Estimated HbA1c: {hba1c_val:.2f}")
    print(f"Estimated glucose: {glucose_val:.2f}")
    
    # Get prediction from compressed model
    prediction_proba = compressed_model.predict_proba(feature_array)[0]
    base_risk = prediction_proba[1] * 100
    
    print(f"\n🎯 COMPRESSED MODEL DIRECT TEST:")
    print(f"Base diabetes probability: {prediction_proba[1]:.6f}")
    print(f"Base risk percentage: {base_risk:.2f}%")
    
    print(f"\n🔄 COMPARISON:")
    print(f"Production API: 0.1%")
    print(f"Local service: 4.1%") 
    print(f"Direct compressed model: {base_risk:.2f}%")
    
    if base_risk < 1.0:
        print(f"\n⚠️ WARNING: Compressed model giving very low risk for multiple risk factors!")
        print(f"This suggests either:")
        print(f"1. Model compression affected accuracy")
        print(f"2. Feature preprocessing is incorrect")
        print(f"3. Training data had insufficient high-risk cases")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()