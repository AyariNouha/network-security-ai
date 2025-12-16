import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_dataset(file_path):
    """Charger dataset CICIDS2017"""
    print(f"📂 Loading dataset from: {file_path}")
    df = pd.read_csv(file_path, encoding='latin1')
    
    # Nettoyer données
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    print(f"✅ Dataset loaded: {len(df)} samples")
    return df

def prepare_features(df):
    """Extraire et normaliser features"""
    
    # Features importantes
    feature_columns = [
        'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
        'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
        'Fwd Packet Length Mean', 'Bwd Packet Length Mean',
        'Flow Bytes/s', 'Flow Packets/s',
        'Fwd Header Length', 'Bwd Header Length'
    ]
    
    # Vérifier colonnes disponibles
    available_features = [col for col in feature_columns if col in df.columns]
    
    if not available_features:
        print("❌ No matching features found!")
        print(f"Available columns: {df.columns.tolist()[:20]}")
        return None, None, None
    
    print(f"✅ Using {len(available_features)} features")
    
    X = df[available_features]
    
    # Label: 0=normal, 1=attack
    if 'Label' in df.columns:
        y = df['Label'].apply(lambda x: 0 if str(x).strip().upper() == 'BENIGN' else 1)
    else:
        y = df.iloc[:, -1].apply(lambda x: 0 if str(x).strip().upper() == 'BENIGN' else 1)
    
    # Normalisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Sauvegarder
    os.makedirs('/app/ml_models', exist_ok=True)
    joblib.dump(scaler, '/app/ml_models/scaler.pkl')
    joblib.dump(available_features, '/app/ml_models/feature_names.pkl')
    
    print(f"✅ Features prepared: {X_scaled.shape}")
    print(f"   Normal samples: {(y==0).sum()}")
    print(f"   Attack samples: {(y==1).sum()}")
    
    return X_scaled, y, available_features