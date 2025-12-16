import sys
sys.path.append('/app/backend')

from monitoring.ml.preprocessing import load_dataset, prepare_features
from monitoring.ml.isolation_forest_model import train_isolation_forest
from monitoring.ml.autoencoder_model import train_autoencoder
from monitoring.ml.lstm_model import train_lstm
from sklearn.model_selection import train_test_split
import os

def train_all():
    """Entraîner tous les modèles ML"""
    
    print("=" * 60)
    print("🚀 AI-ENHANCED NETWORK SECURITY - ML TRAINING PIPELINE")
    print("=" * 60)
    
    # Chemin dataset
    dataset_path = '/app/datasets/CICIDS2017/Monday-WorkingHours.pcap_ISCX.csv'
    
    # Vérifier si dataset existe
    if not os.path.exists(dataset_path):
        print("\n❌ Dataset not found!")
        print(f"   Expected: {dataset_path}")
        print("\n📥 Please download CICIDS2017 dataset:")
        print("   https://www.unb.ca/cic/datasets/ids-2017.html")
        print("\n   Place CSV files in: /app/datasets/CICIDS2017/")
        return
    
    # Charger dataset
    df = load_dataset(dataset_path)
    
    # Préparer features
    X, y, features = prepare_features(df)
    
    if X is None:
        print("❌ Feature preparation failed!")
        return
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Training set: {X_train.shape[0]} samples")
    print(f"📊 Test set: {X_test.shape[0]} samples")
    
    # Séparer données normales pour modèles unsupervised
    X_train_normal = X_train[y_train == 0]
    print(f"📊 Normal training samples: {X_train_normal.shape[0]}")
    
    # Entraîner modèles
    print("\n" + "=" * 60)
    print("TRAINING MODELS")
    print("=" * 60)
    
    # 1. Isolation Forest
    iso_model = train_isolation_forest(X_train_normal)
    
    # 2. Autoencoder
    ae_model = train_autoencoder(X_train_normal, epochs=30)
    
    # 3. LSTM
    lstm_model = train_lstm(X_train, y_train, epochs=15)
    
    print("\n" + "=" * 60)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📁 Models saved in: /app/ml_models/")
    print("   - scaler.pkl")
    print("   - feature_names.pkl")
    print("   - isolation_forest.pkl")
    print("   - autoencoder.h5")
    print("   - lstm_model.h5")

if __name__ == '__main__':
    train_all()
