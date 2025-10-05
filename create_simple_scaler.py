#!/usr/bin/env python3
"""Emergency script to create the simplest possible scaler"""

import pickle
import numpy as np
import os

def create_simple_scaler():
    """Create the simplest scaler possible"""
    
    # Create a simple dictionary instead of StandardScaler
    scaler_data = {
        'means': np.array([41.885856, 27.3207671, 5.527507, 138.05806]),
        'scales': np.array([22.51672729, 6.63675023, 1.07066674, 40.70793251]),
        'feature_names': ['age', 'bmi', 'hbA1c_level', 'blood_glucose_level']
    }
    
    # Save as simple pickle
    scaler_path = 'services/models/simple_scaler.pkl'
    
    print(f"💾 Saving simple scaler to: {scaler_path}")
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler_data, f)
    
    # Verify
    with open(scaler_path, 'rb') as f:
        loaded = pickle.load(f)
    print(f"✅ Verified simple scaler")
    print(f"   Features: {loaded['feature_names']}")
    print(f"   Means: {loaded['means']}")
    
    return scaler_path

if __name__ == "__main__":
    create_simple_scaler()