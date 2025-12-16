import numpy as np
from tensorflow import keras
import os

def prepare_sequences(X, timesteps=10):
    """Préparer séquences temporelles"""
    sequences = []
    for i in range(len(X) - timesteps):
        sequences.append(X[i:i+timesteps])
    return np.array(sequences)

def build_lstm(input_shape):
    """Construire LSTM"""
    
    model = keras.Sequential([
        keras.layers.LSTM(64, return_sequences=True, input_shape=input_shape),
        keras.layers.Dropout(0.3),
        keras.layers.LSTM(32, return_sequences=False),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_lstm(X_train, y_train, timesteps=10, epochs=15):
    """Entraîner LSTM"""
    
    print("\n📈 Training LSTM...")
    
    # Préparer séquences
    X_seq = prepare_sequences(X_train, timesteps)
    y_seq = y_train[timesteps:]
    
    print(f"   Sequences shape: {X_seq.shape}")
    
    model = build_lstm((timesteps, X_train.shape[1]))
    
    # Callbacks
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2
    )
    
    # Entraînement
    history = model.fit(
        X_seq, y_seq,
        epochs=epochs,
        batch_size=128,
        validation_split=0.2,
        callbacks=[early_stop, reduce_lr],
        verbose=1
    )
    
    # Sauvegarder
    os.makedirs('/app/ml_models', exist_ok=True)
    model.save('/app/ml_models/lstm_model.h5')
    
    print("✅ LSTM saved!")
    return model