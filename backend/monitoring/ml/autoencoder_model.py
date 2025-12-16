import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

def build_autoencoder(input_dim):
    """Construire Autoencoder"""
    
    # Encoder
    encoder = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(16, activation='relu')
    ])
    
    # Decoder
    decoder = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(16,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(input_dim, activation='sigmoid')
    ])
    
    # Autoencoder
    autoencoder = keras.Sequential([encoder, decoder])
    autoencoder.compile(optimizer='adam', loss='mse')
    
    return autoencoder

def train_autoencoder(X_train, epochs=30, batch_size=256):
    """Entraîner Autoencoder (seulement sur données normales)"""
    
    print("\n🧠 Training Autoencoder...")
    
    model = build_autoencoder(X_train.shape[1])
    
    # Callbacks
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    
    # Entraînement
    history = model.fit(
        X_train, X_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1
    )
    
    # Sauvegarder
    os.makedirs('/app/ml_models', exist_ok=True)
    model.save('/app/ml_models/autoencoder.h5')
    
    print("✅ Autoencoder saved!")
    return model

def detect_anomaly_autoencoder(model, X, threshold=0.5):
    """Détecter anomalies"""
    reconstructions = model.predict(X, verbose=0)
    mse = np.mean(np.power(X - reconstructions, 2), axis=1)
    return mse > threshold, mse