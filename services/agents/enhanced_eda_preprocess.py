# Enhanced EDA & Preprocessing Pipeline for Diabetes Dataset
# Addresses gaps: year column handling, feature engineering, outlier detection,
# advanced imputation, comprehensive EDA, and high-dimensionality issues

import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder, TargetEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend for compatibility
import matplotlib
matplotlib.use('Agg')

# ---------- Utility Functions ----------
def ensure_dir(p: str):
    """Create directory if it doesn't exist"""
    os.makedirs(p, exist_ok=True)

def is_binary_like(s: pd.Series) -> bool:
    """Check if series contains binary-like values"""
    vals = s.dropna().unique()
    if len(vals) == 2:
        return True
    lowered = pd.Series(vals).astype(str).str.lower().unique()
    return set(lowered).issubset({"yes","no","true","false","positive","negative","pos","neg","y","n","1","0"})

def guess_target(df: pd.DataFrame):
    """Automatically detect target column"""
    common = [
        "Outcome","outcome","target","Target","label","Label","class","Class",
        "diabetes","Diabetes","has_diabetes","diabetic","Diabetic"
    ]
    for c in common:
        if c in df.columns:
            return c
    return None

# ---------- Enhanced EDA Functions ----------
def comprehensive_eda(df: pd.DataFrame, reports_dir: str, target_col: str = None):
    """Enhanced EDA with comprehensive analysis"""
    ensure_dir(reports_dir)
    
    print("🔍 Running Comprehensive EDA...")
    
    # 1. Basic Dataset Info
    basic_info = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicated_rows': df.duplicated().sum()
    }
    
    # 2. Column types and info
    dtypes_df = df.dtypes.astype(str).rename("dtype").reset_index().rename(columns={"index":"column"})
    dtypes_df['unique_values'] = [df[col].nunique() for col in df.columns]
    dtypes_df['null_count'] = [df[col].isnull().sum() for col in df.columns]
    dtypes_df['null_percentage'] = dtypes_df['null_count'].apply(lambda x: round(x / len(df) * 100, 2))
    dtypes_df.to_csv(os.path.join(reports_dir, "01_enhanced_dtypes.csv"), index=False)
    
    # 3. Enhanced missing values analysis with gender-specific context
    miss_analysis = df.isnull().sum().reset_index()
    miss_analysis.columns = ['column', 'missing_count']
    miss_analysis['missing_pct'] = miss_analysis['missing_count'].apply(lambda x: round(x / len(df) * 100, 2))
    
    # Add context for gender-specific features
    miss_analysis['missing_type'] = 'standard'
    gender_specific_features = ['gestational_history', 'gestational_diabetes', 'pregnancy_history']
    
    for feature in gender_specific_features:
        if feature in miss_analysis['column'].values:
            mask = miss_analysis['column'] == feature
            miss_analysis.loc[mask, 'missing_type'] = 'gender_specific'
            
            # If gender column exists, calculate male vs female missing rates
            if 'gender' in df.columns or 'sex' in df.columns:
                gender_col = 'gender' if 'gender' in df.columns else 'sex'
                
                # Calculate missing rates by gender
                gender_stats = []
                for gender_val in df[gender_col].unique():
                    if pd.notna(gender_val):
                        gender_subset = df[df[gender_col] == gender_val]
                        gender_missing = gender_subset[feature].isnull().sum()
                        gender_total = len(gender_subset)
                        gender_pct = round(gender_missing / gender_total * 100, 2) if gender_total > 0 else 0
                        gender_stats.append(f"{gender_val}: {gender_missing}/{gender_total} ({gender_pct}%)")
                
                # Add gender breakdown as a note
                miss_analysis.loc[mask, 'gender_breakdown'] = "; ".join(gender_stats)
    
    # Add gender_breakdown column for non-gender-specific features
    if 'gender_breakdown' not in miss_analysis.columns:
        miss_analysis['gender_breakdown'] = ''
    miss_analysis['gender_breakdown'] = miss_analysis['gender_breakdown'].fillna('')
    
    miss_analysis = miss_analysis.sort_values('missing_pct', ascending=False)
    miss_analysis.to_csv(os.path.join(reports_dir, "02_enhanced_missing_values.csv"), index=False)
    
    # 4. Identify column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Remove target from feature lists if specified
    if target_col and target_col in numeric_cols:
        numeric_cols.remove(target_col)
    if target_col and target_col in categorical_cols:
        categorical_cols.remove(target_col)
    
    # 5. Enhanced numeric analysis
    if numeric_cols:
        numeric_stats = df[numeric_cols].describe()
        
        # Add additional statistics
        numeric_enhanced = numeric_stats.copy()
        for col in numeric_cols:
            data = df[col].dropna()
            numeric_enhanced.loc['skewness', col] = stats.skew(data)
            numeric_enhanced.loc['kurtosis', col] = stats.kurtosis(data)
            numeric_enhanced.loc['cv', col] = data.std() / data.mean() if data.mean() != 0 else 0
        
        numeric_enhanced.round(4).to_csv(os.path.join(reports_dir, "03_enhanced_numeric_analysis.csv"))
    
    # 6. Categorical analysis
    if categorical_cols:
        cat_analysis = []
        for col in categorical_cols:
            unique_vals = df[col].nunique()
            top_category = df[col].mode()[0] if not df[col].mode().empty else 'No Mode'
            top_frequency = df[col].value_counts().iloc[0] if unique_vals > 0 else 0
            
            cat_analysis.append({
                'column': col,
                'unique_categories': unique_vals,
                'top_category': top_category,
                'top_frequency': top_frequency,
                'top_percentage': round(top_frequency / len(df) * 100, 2)
            })
        
        cat_df = pd.DataFrame(cat_analysis)
        cat_df.to_csv(os.path.join(reports_dir, "04_categorical_analysis.csv"), index=False)
    
    # 7. Target distribution (if target specified)
    if target_col and target_col in df.columns:
        target_dist = df[target_col].value_counts().reset_index()
        target_dist.columns = [target_col, 'count']
        target_dist['percentage'] = target_dist['count'].apply(lambda x: round(x / len(df) * 100, 2))
        target_dist.to_csv(os.path.join(reports_dir, "05_target_distribution.csv"), index=False)
    
    # 8. Outlier detection for numeric columns
    outlier_analysis = []
    for col in numeric_cols:
        data = df[col].dropna()
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        outlier_analysis.append({
            'column': col,
            'outlier_count': len(outliers),
            'outlier_percentage': round(len(outliers) / len(data) * 100, 2),
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        })
    
    outlier_df = pd.DataFrame(outlier_analysis)
    outlier_df.to_csv(os.path.join(reports_dir, "06_outlier_analysis.csv"), index=False)
    
    # 9. Correlation analysis (numeric columns only)
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        # Save correlation matrix
        corr_matrix.round(3).to_csv(os.path.join(reports_dir, "07_correlation_matrix.csv"))
        
        # Create correlation heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, linewidths=0.5)
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(os.path.join(reports_dir, "correlation_heatmap.png"), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 10. Generate comprehensive visualizations
    generate_enhanced_visualizations(df, reports_dir, numeric_cols, categorical_cols, target_col)
    
    print(f"✅ Enhanced EDA completed. Reports saved to: {reports_dir}")
    return basic_info

def generate_enhanced_visualizations(df, reports_dir, numeric_cols, categorical_cols, target_col):
    """Generate comprehensive visualizations for all columns"""
    
    # Create visualizations subdirectory
    viz_dir = os.path.join(reports_dir, "visualizations")
    ensure_dir(viz_dir)
    
    # 1. Numeric columns - Histograms and Box plots
    for col in numeric_cols:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Histogram
        df[col].hist(bins=50, ax=axes[0], alpha=0.7, edgecolor='black')
        axes[0].set_title(f'Histogram: {col}')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')
        
        # Box plot
        df.boxplot(column=col, ax=axes[1])
        axes[1].set_title(f'Box Plot: {col}')
        axes[1].set_ylabel(col)
        
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"numeric_{col}.png"), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 2. Categorical columns - Bar plots
    for col in categorical_cols:
        plt.figure(figsize=(12, 6))
        
        # Get value counts
        value_counts = df[col].value_counts()
        
        # Limit to top 20 categories if too many
        if len(value_counts) > 20:
            value_counts = value_counts.head(20)
            title_suffix = " (Top 20)"
        else:
            title_suffix = ""
        
        # Create bar plot
        ax = value_counts.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f'Distribution: {col}{title_suffix}')
        plt.xlabel(col)
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for i, v in enumerate(value_counts.values):
            ax.text(i, v + max(value_counts.values) * 0.01, str(v), 
                   ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"categorical_{col}.png"), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 3. Target vs Features analysis (if target specified)
    if target_col and target_col in df.columns:
        target_viz_dir = os.path.join(viz_dir, "target_analysis")
        ensure_dir(target_viz_dir)
        
        # Numeric features vs target
        for col in numeric_cols:
            plt.figure(figsize=(12, 5))
            
            # Create subplots
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            
            # Box plot by target
            df.boxplot(column=col, by=target_col, ax=axes[0])
            axes[0].set_title(f'{col} by {target_col}')
            
            # Histogram by target
            for target_val in df[target_col].unique():
                subset = df[df[target_col] == target_val][col]
                axes[1].hist(subset, alpha=0.7, label=f'{target_col}={target_val}', bins=30)
            
            axes[1].set_title(f'{col} Distribution by {target_col}')
            axes[1].set_xlabel(col)
            axes[1].set_ylabel('Frequency')
            axes[1].legend()
            
            plt.tight_layout()
            plt.savefig(os.path.join(target_viz_dir, f"target_vs_{col}.png"), dpi=300, bbox_inches='tight')
            plt.close()

# ---------- Enhanced Preprocessing Functions ----------
def detect_outliers_iqr(series, multiplier=1.5):
    """Detect outliers using IQR method"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    return (series < lower_bound) | (series > upper_bound)

def handle_outliers(df, numeric_cols, method='cap', multiplier=1.5):
    """Handle outliers in numeric columns"""
    df_clean = df.copy()
    outlier_info = {}
    
    for col in numeric_cols:
        outliers = detect_outliers_iqr(df_clean[col], multiplier)
        outlier_count = outliers.sum()
        
        if outlier_count > 0:
            if method == 'cap':
                # Cap outliers
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
                
                df_clean[col] = np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
                df_clean[col] = np.where(df_clean[col] > upper_bound, upper_bound, df_clean[col])
                
            elif method == 'remove':
                # Remove outliers (not recommended for large datasets)
                df_clean = df_clean[~outliers]
        
        outlier_info[col] = {
            'outlier_count': outlier_count,
            'outlier_percentage': round(outlier_count / len(df) * 100, 2),
            'method_applied': method if outlier_count > 0 else 'none'
        }
    
    return df_clean, outlier_info

def enhanced_imputation(df, numeric_cols, categorical_cols, target_col=None):
    """Enhanced imputation strategies for different column types"""
    df_imputed = df.copy()
    imputation_info = {}
    
    # Medical/Health-specific imputation logic
    medical_features = ['bmi', 'hbA1c_level', 'blood_glucose_level', 'sleep_hours']
    
    # Numeric imputation
    for col in numeric_cols:
        missing_count = df_imputed[col].isnull().sum()
        
        if missing_count > 0:
            if col in medical_features:
                # For medical features, use median within similar groups if possible
                if target_col and target_col in df.columns:
                    # Group by target and use median
                    df_imputed[col] = df_imputed.groupby(target_col)[col].transform(
                        lambda x: x.fillna(x.median()) if not x.median() != x.median() else x.fillna(df_imputed[col].median())
                    )
                else:
                    df_imputed[col] = df_imputed[col].fillna(df_imputed[col].median())
                imputation_method = 'group_median' if target_col else 'median'
            else:
                # Regular median imputation for other numeric
                df_imputed[col] = df_imputed[col].fillna(df_imputed[col].median())
                imputation_method = 'median'
            
            imputation_info[col] = {
                'missing_count': missing_count,
                'imputation_method': imputation_method
            }
    
    # Categorical imputation
    for col in categorical_cols:
        missing_count = df_imputed[col].isnull().sum()
        
        if missing_count > 0:
            # Special handling for gender-related features like gestational_history
            if col.lower() in ['gestational_history', 'gestational_diabetes', 'pregnancy_history']:
                # For gender-specific features, use gender-aware imputation
                if 'gender' in df_imputed.columns or 'sex' in df_imputed.columns:
                    gender_col = 'gender' if 'gender' in df_imputed.columns else 'sex'
                    # For males, fill with 'Not Applicable' or 'NA'
                    # For females, use mode within female group
                    for gender_val in df_imputed[gender_col].unique():
                        if pd.notna(gender_val):
                            gender_mask = df_imputed[gender_col] == gender_val
                            if gender_val.lower() in ['male', 'm', 'man']:
                                df_imputed.loc[gender_mask, col] = df_imputed.loc[gender_mask, col].fillna('Not Applicable')
                            else:  # female or other
                                female_mode = df_imputed.loc[gender_mask, col].mode()
                                if len(female_mode) > 0:
                                    df_imputed.loc[gender_mask, col] = df_imputed.loc[gender_mask, col].fillna(female_mode[0])
                                else:
                                    df_imputed.loc[gender_mask, col] = df_imputed.loc[gender_mask, col].fillna('No')
                    imputation_method = 'gender_aware'
                else:
                    # If no gender column, assume mixed population and use conservative approach
                    df_imputed[col] = df_imputed[col].fillna('Not Applicable')
                    imputation_method = 'not_applicable'
            else:
                # Regular categorical imputation for non-gender-specific features
                # Use mode or 'Unknown' if no mode exists
                mode_val = df_imputed[col].mode()
                if len(mode_val) > 0:
                    df_imputed[col] = df_imputed[col].fillna(mode_val[0])
                    imputation_method = 'mode'
                else:
                    df_imputed[col] = df_imputed[col].fillna('Unknown')
                    imputation_method = 'unknown'
            
            imputation_info[col] = {
                'missing_count': missing_count,
                'imputation_method': imputation_method
            }
    
    return df_imputed, imputation_info

def feature_engineering(df, target_col=None):
    """Create additional engineered features"""
    df_engineered = df.copy()
    new_features = []
    
    # 1. BMI-related features
    if 'bmi' in df.columns:
        # BMI risk categories (more detailed)
        df_engineered['bmi_risk_level'] = pd.cut(df_engineered['bmi'], 
                                               bins=[0, 18.5, 25, 30, 35, float('inf')],
                                               labels=['underweight', 'normal', 'overweight', 'obese_1', 'obese_2'])
        new_features.append('bmi_risk_level')
    
    # 2. Age-related features
    if 'age' in df.columns:
        # Age risk for diabetes (medical domain knowledge)
        df_engineered['age_diabetes_risk'] = pd.cut(df_engineered['age'],
                                                  bins=[0, 35, 45, 65, float('inf')],
                                                  labels=['low_risk', 'moderate_risk', 'high_risk', 'very_high_risk'])
        new_features.append('age_diabetes_risk')
    
    # 3. Combined health risk score
    health_indicators = ['hypertension', 'heart_disease', 'family_history']
    available_indicators = [col for col in health_indicators if col in df.columns]
    
    if available_indicators:
        df_engineered['health_risk_score'] = df_engineered[available_indicators].sum(axis=1)
        new_features.append('health_risk_score')
    
    # 4. Lifestyle score
    lifestyle_factors = []
    
    # Physical activity scoring
    if 'physical_activity' in df.columns:
        activity_map = {'low': 0, 'moderate': 1, 'high': 2}
        df_engineered['activity_score'] = df_engineered['physical_activity'].map(activity_map).fillna(0)
        lifestyle_factors.append('activity_score')
        new_features.append('activity_score')
    
    # Sleep quality scoring
    if 'sleep_hours' in df.columns:
        # Optimal sleep is 7-9 hours
        df_engineered['sleep_quality'] = df_engineered['sleep_hours'].apply(
            lambda x: 2 if 7 <= x <= 9 else (1 if 6 <= x <= 10 else 0) if pd.notna(x) else 0
        )
        lifestyle_factors.append('sleep_quality')
        new_features.append('sleep_quality')
    
    # Combined lifestyle score
    if lifestyle_factors:
        df_engineered['lifestyle_score'] = df_engineered[lifestyle_factors].sum(axis=1)
        new_features.append('lifestyle_score')
    
    # 5. Geographic risk (if environmental_risk is available)
    if 'environmental_risk' in df.columns and 'urban_rural' in df.columns:
        # Combine environmental risk with urban/rural
        urban_risk_map = {'urban': 1.1, 'rural': 0.9}  # Urban areas might have higher risk
        df_engineered['location_risk'] = (df_engineered['environmental_risk'] * 
                                        df_engineered['urban_rural'].map(urban_risk_map).fillna(1.0))
        new_features.append('location_risk')
    
    return df_engineered, new_features

def handle_high_cardinality_categorical(df, categorical_cols, target_col=None, max_categories=10):
    """Handle high cardinality categorical variables"""
    df_processed = df.copy()
    encoding_info = {}
    
    for col in categorical_cols:
        unique_count = df_processed[col].nunique()
        
        if unique_count > max_categories:
            # For high cardinality columns like 'location' (states)
            if col == 'location':
                # Group by frequency - keep top states, others as 'Other'
                value_counts = df_processed[col].value_counts()
                top_categories = value_counts.head(max_categories).index.tolist()
                df_processed[col] = df_processed[col].apply(
                    lambda x: x if x in top_categories else 'Other'
                )
                encoding_info[col] = {
                    'method': 'frequency_grouping',
                    'kept_categories': len(top_categories) + 1,  # +1 for 'Other'
                    'original_categories': unique_count
                }
            
            elif target_col and target_col in df.columns:
                # Use target encoding for other high cardinality categorical variables
                # This is more sophisticated than frequency grouping
                target_encoder = TargetEncoder()
                df_processed[f'{col}_target_encoded'] = target_encoder.fit_transform(
                    df_processed[[col]], df_processed[target_col]
                )
                
                # Keep original column and add encoded version
                encoding_info[col] = {
                    'method': 'target_encoding',
                    'new_column': f'{col}_target_encoded',
                    'original_categories': unique_count
                }
            else:
                # Fallback to frequency grouping
                value_counts = df_processed[col].value_counts()
                top_categories = value_counts.head(max_categories).index.tolist()
                df_processed[col] = df_processed[col].apply(
                    lambda x: x if x in top_categories else 'Other'
                )
                encoding_info[col] = {
                    'method': 'frequency_grouping',
                    'kept_categories': len(top_categories) + 1,
                    'original_categories': unique_count
                }
    
    return df_processed, encoding_info

def enhanced_preprocessing(df: pd.DataFrame, outdir: str, target_col: str = None, 
                         handle_outliers_method='cap', use_feature_engineering=True):
    """Enhanced preprocessing pipeline with all improvements"""
    ensure_dir(outdir)
    
    print("🔄 Starting Enhanced Preprocessing Pipeline...")
    
    # 1. Initial cleaning
    print("  📋 Step 1: Basic cleaning...")
    df_clean = df.copy()
    initial_shape = df_clean.shape
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    print(f"     Removed {initial_shape[0] - df_clean.shape[0]} duplicate rows")
    
    # 2. Identify column types
    print("  🔍 Step 2: Analyzing column types...")
    numeric_cols = [c for c in df_clean.columns 
                   if pd.api.types.is_numeric_dtype(df_clean[c]) and c != target_col]
    categorical_cols = [c for c in df_clean.columns 
                       if df_clean[c].dtype == "object" and c != target_col]
    
    # Special handling for 'year' column - treat as categorical
    if 'year' in numeric_cols:
        print("     Moving 'year' from numeric to categorical (ordinal treatment)")
        numeric_cols.remove('year')
        categorical_cols.append('year')
        # Convert year to string to treat as categorical
        df_clean['year'] = df_clean['year'].astype(str)
    
    # Special handling for gestational_history - treat as categorical (binary)
    if 'gestational_history' in numeric_cols:
        print("     Moving 'gestational_history' from numeric to categorical (binary treatment)")
        numeric_cols.remove('gestational_history')
        categorical_cols.append('gestational_history')
        # Convert gestational_history to string to treat as categorical, but preserve NaN
        df_clean['gestational_history'] = df_clean['gestational_history'].astype(str)
        df_clean['gestational_history'] = df_clean['gestational_history'].replace('nan', pd.NA)
    
    # 3. Enhanced imputation
    print("  🩹 Step 3: Enhanced imputation...")
    df_clean, imputation_info = enhanced_imputation(df_clean, numeric_cols, categorical_cols, target_col)
    
    # Save imputation info
    imputation_df = pd.DataFrame.from_dict(imputation_info, orient='index').reset_index()
    imputation_df.columns = ['column', 'missing_count', 'imputation_method']
    imputation_df.to_csv(os.path.join(outdir, "imputation_report.csv"), index=False)
    
    # 4. Outlier handling for numeric columns
    if numeric_cols and handle_outliers_method != 'none':
        print(f"  🎯 Step 4: Handling outliers using {handle_outliers_method} method...")
        df_clean, outlier_info = handle_outliers(df_clean, numeric_cols, handle_outliers_method)
        
        # Save outlier info
        outlier_df = pd.DataFrame.from_dict(outlier_info, orient='index').reset_index()
        outlier_df.to_csv(os.path.join(outdir, "outlier_treatment_report.csv"), index=False)
    
    # 5. Feature Engineering
    if use_feature_engineering:
        print("  ⚙️  Step 5: Feature engineering...")
        df_clean, new_features = feature_engineering(df_clean, target_col)
        print(f"     Created {len(new_features)} new features: {new_features}")
        
        # Update column lists with new categorical features
        new_categorical = [f for f in new_features if df_clean[f].dtype == 'object']
        categorical_cols.extend(new_categorical)
        
        new_numeric = [f for f in new_features if f not in new_categorical]
        numeric_cols.extend(new_numeric)
    
    # 6. Handle high cardinality categorical variables
    print("  📊 Step 6: Handling high cardinality categorical variables...")
    df_clean, encoding_info = handle_high_cardinality_categorical(
        df_clean, categorical_cols, target_col, max_categories=15
    )
    
    # Save encoding info
    if encoding_info:
        encoding_df = pd.DataFrame.from_dict(encoding_info, orient='index').reset_index()
        encoding_df.to_csv(os.path.join(outdir, "encoding_report.csv"), index=False)
    
    # 7. Save human-readable version
    print("  💾 Step 7: Saving human-readable version...")
    readable_path = os.path.join(outdir, "diabetes_enhanced_readable.csv")
    df_clean.to_csv(readable_path, index=False)
    
    # 8. Prepare ML-ready version
    print("  🤖 Step 8: Preparing ML-ready version...")
    df_ml = df_clean.copy()
    
    # Get updated categorical columns (excluding target encoded columns for one-hot encoding)
    categorical_for_encoding = [col for col in categorical_cols 
                               if not any(f'{col}_target_encoded' in colname for colname in df_ml.columns)]
    
    # One-hot encoding for categorical variables
    if categorical_for_encoding:
        print(f"     Applying one-hot encoding to: {categorical_for_encoding}")
        df_ml = pd.get_dummies(df_ml, columns=categorical_for_encoding, drop_first=False)
    
    # Update numeric columns list (include target encoded features, exclude categorical features)
    target_encoded_cols = [col for col in df_ml.columns if 'target_encoded' in col]
    
    # Filter numeric_cols to only include truly numeric columns that exist in df_ml
    final_numeric_cols = []
    for col in numeric_cols:
        if col in df_ml.columns and pd.api.types.is_numeric_dtype(df_ml[col]):
            final_numeric_cols.append(col)
    
    # Add target encoded columns
    final_numeric_cols.extend(target_encoded_cols)
    
    # 9. Scaling numeric features (excluding year which is now categorical)
    scaler = None  # Initialize scaler variable
    if final_numeric_cols:
        print(f"     Scaling {len(final_numeric_cols)} numeric features...")
        scaler = StandardScaler()
        df_ml[final_numeric_cols] = scaler.fit_transform(df_ml[final_numeric_cols])
        print(f"     Scaling completed for: {final_numeric_cols}")
    
    # 10. Feature selection (optional - select top K features for numeric columns only)
    feature_selection_applied = False
    if target_col and target_col in df_ml.columns and len(df_ml.columns) > 50:
        print("  🎯 Step 9: Feature selection (too many features detected)...")
        feature_selection_applied = True
        
        # Separate features and target
        X = df_ml.drop(columns=[target_col])
        y = df_ml[target_col]
        
        # Only apply feature selection to numeric columns
        numeric_feature_cols = [col for col in X.columns if pd.api.types.is_numeric_dtype(X[col])]
        categorical_feature_cols = [col for col in X.columns if not pd.api.types.is_numeric_dtype(X[col])]
        
        # Protect medically important features from being dropped
        protected_features = [col for col in X.columns if any(term in col.lower() for term in 
                             ['gestational', 'pregnancy', 'hba1c', 'glucose', 'bmi', 'age'])]
        
        protected_numeric = [col for col in protected_features if col in numeric_feature_cols]
        selectable_numeric = [col for col in numeric_feature_cols if col not in protected_numeric]
        
        if selectable_numeric and len(numeric_feature_cols) > 30:
            # Select from non-protected numeric features
            k_selectable = max(1, min(15, len(selectable_numeric)))  # Select fewer from non-protected
            
            selector = SelectKBest(score_func=f_classif, k=k_selectable)
            X_selectable_selected = selector.fit_transform(X[selectable_numeric], y)
            
            # Get selected feature names from selectable features
            selected_selectable_features = pd.Series(selectable_numeric)[selector.get_support()].tolist()
            
            # Combine protected features + selected features + all categorical features + target
            selected_features = protected_numeric + selected_selectable_features + categorical_feature_cols + [target_col]
            
            df_ml = df_ml[selected_features]
            
            # Save feature selection info
            feature_scores = pd.DataFrame({
                'feature': selectable_numeric,
                'score': selector.scores_,
                'selected': selector.get_support(),
                'protected': False
            })
            
            # Add protected features info
            protected_df = pd.DataFrame({
                'feature': protected_numeric,
                'score': 999,  # High score to indicate protection
                'selected': True,
                'protected': True
            })
            
            feature_scores = pd.concat([protected_df, feature_scores]).sort_values('score', ascending=False)
            feature_scores.to_csv(os.path.join(outdir, "feature_selection_report.csv"), index=False)
            
            print(f"     Protected {len(protected_numeric)} medical features, selected {k_selectable} from {len(selectable_numeric)} others")
            print(f"     Kept all {len(categorical_feature_cols)} categorical features")
        else:
            print("     Skipping feature selection - not enough numeric features or features already manageable")
            feature_selection_applied = False
    
    # Save scaler after feature selection (so it only contains final numeric features)
    if scaler is not None:
        print("  💾 Step 10: Saving feature scaler...")
        # Determine final numeric features that remain in the dataset
        final_numeric_in_ml = [col for col in df_ml.columns 
                              if col in final_numeric_cols and col != target_col]
        
        if final_numeric_in_ml:
            print(f"     Saving scaler for final {len(final_numeric_in_ml)} numeric features...")
            # Create a new scaler fitted only on the final features
            final_scaler = StandardScaler()
            final_scaler.fit(df_ml[final_numeric_in_ml])
            
            import joblib
            scaler_path = os.path.join(outdir, "feature_scaler.pkl")
            joblib.dump(final_scaler, scaler_path)
            print(f"     Final scaler saved to: {scaler_path}")
            print(f"     Scaler contains features: {final_numeric_in_ml}")
        else:
            print("     No numeric features remaining - scaler not saved")
    
    # 11. Save ML-ready version
    print("  💾 Step 11: Saving ML-ready version...")
    ml_path = os.path.join(outdir, "diabetes_enhanced_ml_ready.csv")
    df_ml.to_csv(ml_path, index=False)
    
    # 12. Generate processing summary
    processing_summary = {
        'original_rows': initial_shape[0],
        'original_columns': initial_shape[1],
        'final_rows': df_ml.shape[0],
        'final_columns': df_ml.shape[1],
        'duplicates_removed': initial_shape[0] - df_clean.shape[0],
        'numeric_features': len([c for c in final_numeric_cols if c in df_ml.columns]),
        'categorical_features_encoded': len(categorical_for_encoding),
        'new_features_created': len(new_features) if use_feature_engineering else 0,
        'outlier_method': handle_outliers_method,
        'feature_selection_applied': 'Yes' if len(df_ml.columns) != len(df_clean.columns) else 'No',
        'total_final_features': len(df_ml.columns) - (1 if target_col in df_ml.columns else 0)
    }
    
    summary_df = pd.DataFrame.from_dict(processing_summary, orient='index', columns=['value'])
    summary_df.to_csv(os.path.join(outdir, "processing_summary.csv"))
    
    print(f"✅ Enhanced preprocessing completed!")
    print(f"   📁 Human-readable data: {readable_path}")
    print(f"   🤖 ML-ready data: {ml_path}")
    print(f"   📊 Final dataset: {df_ml.shape[0]} rows × {df_ml.shape[1]} columns")
    
    return readable_path, ml_path, processing_summary

# ---------- Main Function ----------
def main():
    parser = argparse.ArgumentParser(description="Enhanced EDA + Preprocessing for Diabetes Dataset")
    parser.add_argument("--input", required=True, help="Path to raw CSV file")
    parser.add_argument("--outdir", default="data/processed_enhanced", help="Output directory for processed files")
    parser.add_argument("--reports", default="data/reports_enhanced", help="Output directory for EDA reports")
    parser.add_argument("--target", default=None, help="Target column name (auto-detected if not provided)")
    parser.add_argument("--outliers", default="cap", choices=["cap", "remove", "none"], 
                       help="Outlier handling method")
    parser.add_argument("--no-feature-engineering", action="store_true", 
                       help="Skip feature engineering step")
    
    args = parser.parse_args()
    
    print("🚀 Starting Enhanced Diabetes Dataset Analysis Pipeline")
    print("=" * 60)
    
    # Load dataset
    print(f"📂 Loading dataset from: {args.input}")
    df = pd.read_csv(args.input)
    print(f"   Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Auto-detect target if not provided
    target_col = args.target or guess_target(df)
    if target_col:
        print(f"🎯 Target column: {target_col}")
    else:
        print("⚠️  No target column detected")
    
    print("\n" + "=" * 60)
    
    # Run enhanced EDA
    basic_info = comprehensive_eda(df, reports_dir=args.reports, target_col=target_col)
    
    print("\n" + "=" * 60)
    
    # Run enhanced preprocessing
    readable_path, ml_path, summary = enhanced_preprocessing(
        df, 
        outdir=args.outdir, 
        target_col=target_col,
        handle_outliers_method=args.outliers,
        use_feature_engineering=not args.no_feature_engineering
    )
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline completed successfully!")
    print(f"📊 EDA reports available in: {args.reports}")
    print(f"📁 Processed data available in: {args.outdir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
