import joblib
import numpy as np
from tensorflow import keras
import os

class AnomalyPredictor:
    def __init__(self):
        model_path = '/app/ml_models'
        
        print("🔄 Loading ML models...")
        
        # Charger modèles
        self.scaler = joblib.load(f'{model_path}/scaler.pkl')
        self.feature_names = joblib.load(f'{model_path}/feature_names.pkl')
        self.iso_forest = joblib.load(f'{model_path}/isolation_forest.pkl')
        self.autoencoder = keras.models.load_model(f'{model_path}/autoencoder.h5')
        
        print("✅ ML models loaded successfully!")
    
    def predict(self, features):
        """Prédire si un flow est une anomalie"""
        
        # Vérifier nombre de features
        if len(features) != len(self.feature_names):
            print(f"⚠️  Expected {len(self.feature_names)} features, got {len(features)}")
            return False, {'error': 'Invalid number of features'}
        
        # Normaliser
        X = self.scaler.transform([features])
        
        # 1. Isolation Forest
        iso_pred = self.iso_forest.predict(X)[0]  # -1 = anomalie, 1 = normal
        
        # 2. Autoencoder
        ae_reconstruction = self.autoencoder.predict(X, verbose=0)
        ae_mse = np.mean(np.power(X - ae_reconstruction, 2))
        ae_pred = 1 if ae_mse > 0.5 else 0
        
        # Vote majoritaire
        is_anomaly = (iso_pred == -1) or (ae_pred == 1)
        
        # Calcul confiance
        if iso_pred == -1 and ae_pred == 1:
            confidence = 0.95  # Les deux détectent anomalie
        elif iso_pred == -1 or ae_pred == 1:
            confidence = 0.75  # Un seul détecte
        else:
            confidence = 0.90  # Normal
        
        return is_anomaly, {
            'isolation_forest': 'anomaly' if iso_pred == -1 else 'normal',
            'autoencoder_mse': float(ae_mse),
            'autoencoder': 'anomaly' if ae_pred == 1 else 'normal',
            'confidence': confidence
        }