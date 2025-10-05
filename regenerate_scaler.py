#!/usr/bin/env python3
"""
Quick script to regenerate the feature scaler correctly
"""

import pandas as pd
import numpy as np
import pickle
import joblib
import os
from sklearn.preprocessing import StandardScaler

def regenerate_scaler():
    """Regenerate the feature scaler correctly"""
    
    print("🔄 REGENERATING FEATURE SCALER")
    print("=" * 40)
    
    # Load the raw data
    raw_data_path = 'services/data/raw/diabetes_dataset_E.csv'
    
    if not os.path.exists(raw_data_path):
        print(f"❌ Raw data not found: {raw_data_path}")
        return
    
    print(f"📁 Loading raw data from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    
    print(f"   Data shape: {df.shape}")
    print(f"   Columns: {df.columns.tolist()}")
    
    # Identify numeric columns (the ones we need to scale)
    numeric_cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    
    # Check if columns exist (handle case variations)
    available_numeric = []
    for col in numeric_cols:
        # Try exact match first
        if col in df.columns:
            available_numeric.append(col)
        else:
            # Try case-insensitive match
            for df_col in df.columns:
                if col.lower() == df_col.lower():
                    available_numeric.append(df_col)
                    break
    
    print(f"📊 Found numeric columns: {available_numeric}")
    
    if not available_numeric:
        print("❌ No numeric columns found!")
        return
    
    # Create and fit the scaler on the raw (unscaled) data
    print(f"🔧 Creating StandardScaler for {len(available_numeric)} features...")
    
    scaler = StandardScaler()
    scaler.fit(df[available_numeric])
    
    print(f"✅ Scaler fitted successfully")
    print(f"   Features: {available_numeric}")
    print(f"   Means: {scaler.mean_}")
    print(f"   Scales: {scaler.scale_}")
    
    # Save the scaler
    output_dir = 'services/data/processed_enhanced'
    os.makedirs(output_dir, exist_ok=True)
    
    scaler_path = os.path.join(output_dir, 'feature_scaler.pkl')
    
    print(f"💾 Saving scaler to: {scaler_path}")
    joblib.dump(scaler, scaler_path)
    
    # Verify the saved scaler
    print(f"🧪 Verifying saved scaler...")
    loaded_scaler = joblib.load(scaler_path)
    
    print(f"   Type: {type(loaded_scaler)}")
    print(f"   Features: {loaded_scaler.n_features_in_}")
    print(f"   Means: {loaded_scaler.mean_}")
    print(f"   Scales: {loaded_scaler.scale_}")
    
    # Test with sample data
    test_data = np.array([[25, 22.04, 5.5, 95]])  # age, bmi, hbA1c, glucose
    print(f"\n🧪 Testing with sample data: {test_data[0]}")
    
    scaled_data = loaded_scaler.transform(test_data)
    print(f"   Scaled data: {scaled_data[0]}")
    
    print(f"\n✅ Scaler regenerated successfully!")
    
    return scaler_path

if __name__ == "__main__":
    regenerate_scaler()