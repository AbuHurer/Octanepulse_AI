import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

def train_model():
    """Load processed data, train a classification model, and save it."""
    data_path = os.path.join('data', 'processed', 'clean_fights.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed data not found at {data_path}. Please run src/etl.py first!")
    
    print(f"Loading processed data from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Separate features and target
    X = df.drop(columns=['target'])
    y = df['target']
    
    print(f"Features shape: {X.shape}")
    print(f"Target class distribution:\n{y.value_counts(normalize=True)}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print("\n--- Model Evaluation Results ---")
    print(f"Accuracy: {acc:.4f}")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'fight_predictor_model.joblib')
    
    # Save model and feature columns list (for API inference alignment)
    model_artifact = {
        'model': model,
        'feature_columns': list(X.columns)
    }
    
    joblib.dump(model_artifact, model_path)
    print(f"\nSuccessfully saved trained model artifact to {model_path}!")

if __name__ == "__main__":
    train_model()