import os
import pandas as pd
import numpy as np

def parse_height_to_inches(height_str):
    """Convert height string like '5\' 9"' or '6\' 1"' into total inches."""
    if pd.isna(height_str) or not isinstance(height_str, str):
        return np.nan
    try:
        parts = height_str.replace('"', '').split("'")
        feet = float(parts[0].strip())
        inches = float(parts[1].strip()) if len(parts) > 1 and parts[1].strip() != '' else 0.0
        return (feet * 12) + inches
    except Exception:
        return np.nan

def load_data():
    """Load raw master dataset."""
    master_path = os.path.join('data', 'raw', 'master.csv')
    if not os.path.exists(master_path):
        master_path = 'master.csv'
    
    print(f"Loading data from {master_path}...")
    df = pd.read_csv(master_path)
    return df

def preprocess_data(df):
    """Clean data and engineer features for fight outcome prediction."""
    print("Preprocessing data and engineering features...")
    df = df.copy()
    
    # Drop rows where winner_id is missing
    df = df.dropna(subset=['winner_id'])
    
    # Create target column: 1 if Red wins, 0 if Blue wins
    df['target'] = np.where(df['winner_id'] == df['r_fighter_id'], 1, 0)
    
    # Convert height strings to inches
    df['r_height_inches'] = df['r_height'].apply(parse_height_to_inches)
    df['b_height_inches'] = df['b_height'].apply(parse_height_to_inches)
    
    # 1. Physical differentials
    df['height_diff'] = df['r_height_inches'] - df['b_height_inches']
    df['weight_diff'] = df['r_weight_lbs'] - df['b_weight_lbs']
    df['reach_diff'] = df['r_reach_inches'] - df['b_reach_inches']
    
    # 2. Striking differentials
    df['slpm_diff'] = df['r_slpm'] - df['b_slpm']
    df['str_acc_diff'] = df['r_str_acc'] - df['b_str_acc']
    df['sapm_diff'] = df['r_sapm'] - df['b_sapm']
    df['str_def_diff'] = df['r_str_def'] - df['b_str_def']
    
    # 3. Grappling differentials
    df['td_avg_diff'] = df['r_td_avg'] - df['b_td_avg']
    df['td_acc_diff'] = df['r_td_acc'] - df['b_td_acc']
    df['td_def_diff'] = df['r_td_def'] - df['b_td_def']
    df['sub_avg_diff'] = df['r_sub_avg'] - df['b_sub_avg']
    
    # Select final feature subset for modeling + target
    feature_columns = [
        'height_diff', 'weight_diff', 'reach_diff',
        'slpm_diff', 'str_acc_diff', 'sapm_diff', 'str_def_diff',
        'td_avg_diff', 'td_acc_diff', 'td_def_diff', 'sub_avg_diff',
        'target'
    ]
    
    # Keep only these columns and drop any remaining rows with NaNs
    df_model = df[feature_columns].dropna()
    
    print(f"Processed dataset shape: {df_model.shape}")
    return df_model

if __name__ == "__main__":
    df_raw = load_data()
    df_clean = preprocess_data(df_raw)
    
    os.makedirs('data/processed', exist_ok=True)
    output_path = os.path.join('data', 'processed', 'clean_fights.csv')
    df_clean.to_csv(output_path, index=False)
    print(f"Successfully saved cleaned data to {output_path}!")