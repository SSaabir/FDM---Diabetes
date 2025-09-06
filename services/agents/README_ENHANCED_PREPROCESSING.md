# Enhanced EDA & Preprocessing Pipeline

This directory contains the enhanced version of the EDA and preprocessing pipeline that addresses all gaps identified in the original implementation.

## Quick Start

### Run Enhanced Preprocessing

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run enhanced preprocessing
python agents/enhanced_eda_preprocess.py --input "data/raw/diabetes_dataset_E.csv" --outdir "data/processed_enhanced" --reports "data/reports_enhanced" --target "diabetes"
```

### Compare Results

```bash
# Compare original vs enhanced preprocessing
python agents/compare_preprocessing.py
```

## Key Improvements

### ✅ Fixed Issues from Original
1. **Year Column Scaling**: Fixed incorrect scaling of year column (now treated as categorical)
2. **Limited EDA**: Expanded from 6 histograms to comprehensive analysis
3. **No Feature Engineering**: Added 7 domain-specific engineered features
4. **Basic Imputation**: Implemented medical domain-aware imputation
5. **No Outlier Handling**: Added IQR-based outlier detection and capping
6. **High Dimensionality**: Intelligent handling of high-cardinality categorical variables

### 🔬 Enhanced EDA Features
- **Complete Statistical Analysis**: All columns analyzed with advanced statistics
- **Outlier Detection**: IQR-based outlier identification and reporting
- **Correlation Analysis**: Full correlation matrix with visualizations
- **Target Relationship**: Detailed target vs feature analysis
- **Comprehensive Visualizations**: All features visualized appropriately

### ⚙️ Advanced Preprocessing
- **Smart Feature Engineering**: 7 new features based on medical domain knowledge
- **Outlier Handling**: Configurable outlier treatment (cap/remove/none)
- **Enhanced Imputation**: Group-based imputation for medical features
- **Dimensionality Control**: Feature selection and category grouping
- **Proper Data Types**: Correct handling of categorical vs numeric features

## Generated Files

### EDA Reports (`data/reports_enhanced/`)
```
01_enhanced_dtypes.csv              - Extended data type analysis
02_enhanced_missing_values.csv     - Comprehensive missing value analysis
03_enhanced_numeric_analysis.csv   - Advanced numeric statistics
04_categorical_analysis.csv        - Categorical feature analysis
05_target_distribution.csv         - Target variable distribution
06_outlier_analysis.csv           - Outlier detection results
07_correlation_matrix.csv         - Feature correlation matrix
correlation_heatmap.png           - Correlation visualization
visualizations/                   - Complete visual analysis
  ├── numeric_*.png              - Histograms and box plots for all numeric features
  ├── categorical_*.png          - Bar charts for all categorical features
  └── target_analysis/           - Target vs feature relationships
ENHANCEMENT_SUMMARY.md           - Comprehensive improvement summary
```

### Processed Data (`data/processed_enhanced/`)
```
diabetes_enhanced_readable.csv      - Human-readable processed data
diabetes_enhanced_ml_ready.csv      - ML-ready scaled and encoded data
feature_scaler.pkl                  - Saved StandardScaler for predictions
processing_summary.csv              - Processing statistics summary
imputation_report.csv              - Imputation methods used
outlier_treatment_report.csv       - Outlier handling details
encoding_report.csv                - High cardinality handling methods
feature_selection_report.csv       - Feature selection results and scores
```

## Command Line Options

```bash
python agents/enhanced_eda_preprocess.py --help
```

Available options:
- `--input`: Path to raw CSV file (required)
- `--outdir`: Output directory for processed files
- `--reports`: Output directory for EDA reports  
- `--target`: Target column name (auto-detected if not provided)
- `--outliers`: Outlier handling method (cap/remove/none)
- `--no-feature-engineering`: Skip feature engineering step

## Feature Engineering Details

### New Features Created:
1. **bmi_risk_level**: Detailed BMI risk categorization
2. **age_diabetes_risk**: Age-based diabetes risk groups  
3. **health_risk_score**: Combined health conditions score
4. **activity_score**: Physical activity level scoring
5. **sleep_quality**: Sleep quality assessment
6. **lifestyle_score**: Combined lifestyle factors
7. **location_risk**: Geographic risk (environmental × urban/rural)

## Model Training Recommendations

### For the Model Training Team:

1. **Use Enhanced Dataset**: `diabetes_enhanced_ml_ready.csv`
2. **Load Scaler**: Use `feature_scaler.pkl` for consistent preprocessing
3. **Feature Selection**: Review `feature_selection_report.csv` for feature importance
4. **Cross-Validation**: Implement proper CV with the processed data
5. **Regularization**: Still apply L1/L2 to prevent overfitting
6. **Model Comparison**: Try multiple algorithms with enhanced features

### Expected Improvements:
- **Reduced Overfitting**: Feature selection and outlier handling
- **Better Features**: Domain-specific engineered features
- **Correct Data Types**: Proper categorical/numeric treatment
- **Cleaner Data**: Advanced imputation and outlier treatment

## Technical Details

### Dependencies:
```
pandas>=2.1.3
numpy>=1.25.2  
scipy>=1.11.4
scikit-learn>=1.3.2
matplotlib>=3.8.2
seaborn>=0.13.0
joblib
```

### Processing Pipeline:
1. **Data Loading & Validation**
2. **Column Type Identification** (with year correction)
3. **Advanced Imputation** (medical domain-aware)
4. **Outlier Detection & Treatment** 
5. **Feature Engineering** (7 new features)
6. **High Cardinality Handling** (grouping/encoding)
7. **One-Hot Encoding**
8. **Feature Scaling** (numeric only)
9. **Feature Selection** (if >50 features)
10. **Export & Documentation**

## Comparison with Original

| Aspect | Original | Enhanced |
|--------|----------|----------|
| Dataset Size | 100K × 28 | 100K × 23 (selected) |
| Year Handling | ❌ Scaled incorrectly | ✅ Categorical |
| EDA Scope | ❌ 6 basic plots | ✅ Comprehensive |
| Feature Engineering | ❌ None | ✅ 7 new features |
| Outlier Handling | ❌ None | ✅ IQR capping |
| Feature Selection | ❌ None | ✅ Statistical selection |
| Documentation | ❌ Basic | ✅ Complete reports |

## Next Steps

1. **Model Training**: Use enhanced dataset with proper cross-validation
2. **Performance Comparison**: Compare model performance vs original data
3. **Feature Analysis**: Analyze importance of engineered features
4. **Production Pipeline**: Adapt enhanced preprocessing for real-time predictions

## Support

For questions about the enhanced preprocessing pipeline, refer to:
- `ENHANCEMENT_SUMMARY.md` - Detailed improvement analysis
- Generated reports in `data/reports_enhanced/`  
- Processing logs and statistics in `data/processed_enhanced/`
