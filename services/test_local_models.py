import joblib
import json
import numpy as np
import pandas as pd

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

print("🔍 Testing local models with high-risk case:")
print(f"Input: {user_input}")
print("\n" + "="*60)

try:
    # Load compressed models
    print("📂 Loading compressed models...")
    general_model = joblib.load('models/diabetes_general_model_compressed_lvl3.pkl')
    women_model = joblib.load('models/diabetes_women_model.pkl')  # Use regular women model
    
    # Load feature lists
    with open('models/general_model_features.json', 'r') as f:
        general_features_data = json.load(f)
        general_features = general_features_data['features']
    
    with open('models/women_model_features.json', 'r') as f:
        women_features_data = json.load(f)
        women_features = women_features_data['features']
        
    print(f"✅ Models loaded successfully")
    print(f"General model features: {len(general_features)}")
    print(f"Women model features: {len(women_features)}")
    
    # Calculate BMI
    height_m = user_input['height'] / 100
    bmi = user_input['weight'] / (height_m ** 2)
    print(f"\n📊 BMI: {bmi:.2f}")
    
    # Create feature vector for general model
    print(f"\n🧮 Creating feature vector...")
    features_dict = {}
    
    # Initialize all features to 0
    for feature in general_features:
        features_dict[feature] = 0.0
    
    # Normalize age (using standard normalization)
    age_normalized = (user_input['age'] - 41.89) / 22.52  # Mean and std from training
    features_dict['age'] = age_normalized
    
    # Normalize BMI
    bmi_normalized = (bmi - 27.32) / 6.64  # Mean and std from training
    features_dict['bmi'] = bmi_normalized
    
    # Estimate HbA1c and glucose based on risk factors
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
    
    # Normalize HbA1c and glucose
    hba1c_normalized = (hba1c_val - 5.53) / 1.07
    glucose_normalized = (glucose_val - 138.06) / 40.71
    
    features_dict['hbA1c_level'] = hba1c_normalized
    features_dict['blood_glucose_level'] = glucose_normalized
    
    print(f"Estimated HbA1c: {hba1c_val:.2f} (normalized: {hba1c_normalized:.3f})")
    print(f"Estimated glucose: {glucose_val:.2f} (normalized: {glucose_normalized:.3f})")
    
    # Gender
    if user_input['gender'].lower() == 'male':
        features_dict['gender_Male'] = 1.0
    elif user_input['gender'].lower() == 'female':
        features_dict['gender_Female'] = 1.0
        
    # Smoking history
    if user_input['smoking'] == 'yes':
        features_dict['smoking_history_current'] = 1.0
    else:
        features_dict['smoking_history_never'] = 1.0
        
    # BMI categories
    if bmi < 18.5:
        features_dict['bmi_category_Underweight'] = 1.0
        features_dict['bmi_risk_level_underweight'] = 1.0
    elif bmi < 25:
        features_dict['bmi_category_Normal'] = 1.0
        features_dict['bmi_risk_level_normal'] = 1.0
    elif bmi < 30:
        features_dict['bmi_category_Overweight'] = 1.0
        features_dict['bmi_risk_level_overweight'] = 1.0
    elif bmi < 35:
        features_dict['bmi_category_Obese'] = 1.0
        features_dict['bmi_risk_level_obese_1'] = 1.0
    else:
        features_dict['bmi_category_Obese'] = 1.0
        features_dict['bmi_risk_level_obese_2'] = 1.0
        
    # Age groups
    if user_input['age'] < 18:
        features_dict['age_group_Child'] = 1.0
    elif user_input['age'] < 40:
        features_dict['age_group_Adult'] = 1.0
    elif user_input['age'] < 60:
        features_dict['age_group_Middle-aged'] = 1.0
    else:
        features_dict['age_group_Senior'] = 1.0
        
    # Age diabetes risk
    if user_input['age'] >= 65:
        features_dict['age_diabetes_risk_high_risk'] = 1.0
    elif user_input['age'] >= 45:
        features_dict['age_diabetes_risk_moderate_risk'] = 1.0
    else:
        features_dict['age_diabetes_risk_low_risk'] = 1.0
        
    print(f"\n🔧 Feature vector created with {len([k for k, v in features_dict.items() if v != 0])} non-zero features")
    
    # Convert to array in correct order
    feature_array = np.array([[features_dict[feature] for feature in general_features]])
    
    print(f"Feature array shape: {feature_array.shape}")
    
    # Get prediction
    prediction_proba = general_model.predict_proba(feature_array)[0]
    risk_percentage = prediction_proba[1] * 100
    
    print(f"\n🎯 MODEL OUTPUT:")
    print(f"No diabetes probability: {prediction_proba[0]:.6f} ({prediction_proba[0]*100:.2f}%)")
    print(f"Diabetes probability: {prediction_proba[1]:.6f} ({prediction_proba[1]*100:.2f}%)")
    print(f"Final risk percentage: {risk_percentage:.2f}%")
    
    # Show important features
    print(f"\n📋 Key Features Used:")
    important_features = {k: v for k, v in features_dict.items() if abs(v) > 0.001}
    for feature, value in sorted(important_features.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"  {feature}: {value:.3f}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()