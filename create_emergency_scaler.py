import numpy as np
import pandas as pd
from pathlib import Path
import joblib

def create_emergency_scaler():
    """Create emergency scaler directly in models directory"""
    
    print("🚨 CREATING EMERGENCY SCALER")
    
    # Quick scaler with the exact stats we know work
    from sklearn.preprocessing import StandardScaler
    
    # Create scaler with our known good parameters
    scaler = StandardScaler()
    
    # Fit with sample data to set the parameters we need
    sample_data = pd.DataFrame({
        'age': [41.885856],
        'bmi': [27.3207671], 
        'hbA1c_level': [5.527507],
        'blood_glucose_level': [138.05806]
    })
    
    scaler.fit(sample_data)
    
    # Manually set the correct statistics
    scaler.mean_ = np.array([41.885856, 27.3207671, 5.527507, 138.05806])
    scaler.scale_ = np.array([22.51672729, 6.63675023, 1.07066674, 40.70793251])
    scaler.var_ = scaler.scale_ ** 2
    scaler.n_features_in_ = 4
    scaler.feature_names_in_ = np.array(['age', 'bmi', 'hbA1c_level', 'blood_glucose_level'])
    
    # Save to models directory
    models_path = Path('services/models')
    scaler_path = models_path / 'feature_scaler.pkl'
    
    print(f"💾 Saving emergency scaler to: {scaler_path}")
    joblib.dump(scaler, scaler_path)
    
    # Verify
    loaded = joblib.load(scaler_path)
    print(f"✅ Verified: {loaded.n_features_in_} features")
    print(f"✅ Features: {list(loaded.feature_names_in_)}")
    print(f"✅ Means: {loaded.mean_}")
    
    return scaler_path

if __name__ == "__main__":
    create_emergency_scaler()