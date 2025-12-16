from sklearn.ensemble import IsolationForest
import joblib
import os

def train_isolation_forest(X_train):
    """Entraîner Isolation Forest (seulement sur données normales)"""
    
    print("\n🌲 Training Isolation Forest...")
    
    model = IsolationForest(
        contamination=0.1,
        random_state=42,
        n_estimators=100,
        max_samples='auto',
        n_jobs=-1
    )
    
    model.fit(X_train)
    
    # Sauvegarder
    os.makedirs('/app/ml_models', exist_ok=True)
    joblib.dump(model, '/app/ml_models/isolation_forest.pkl')
    
    print("✅ Isolation Forest saved!")
    return model

def predict_anomaly(model, X):
    """Prédire anomalies"""
    predictions = model.predict(X)
    # -1 = anomalie, 1 = normal
    return predictions