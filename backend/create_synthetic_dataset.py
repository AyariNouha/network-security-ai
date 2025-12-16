import pandas as pd
import numpy as np
import os

# Créer dataset synthétique pour test
np.random.seed(42)

n_samples = 10000

data = {
    'Flow Duration': np.random.randint(0, 1000000, n_samples),
    'Total Fwd Packets': np.random.randint(1, 100, n_samples),
    'Total Backward Packets': np.random.randint(1, 100, n_samples),
    'Total Length of Fwd Packets': np.random.randint(0, 50000, n_samples),
    'Total Length of Bwd Packets': np.random.randint(0, 50000, n_samples),
    'Fwd Packet Length Mean': np.random.uniform(0, 1500, n_samples),
    'Bwd Packet Length Mean': np.random.uniform(0, 1500, n_samples),
    'Flow Bytes/s': np.random.uniform(0, 100000, n_samples),
    'Flow Packets/s': np.random.uniform(0, 1000, n_samples),
    'Fwd Header Length': np.random.randint(20, 60, n_samples),
    'Bwd Header Length': np.random.randint(20, 60, n_samples),
    'Label': np.random.choice(['BENIGN', 'DDoS', 'PortScan'], n_samples, p=[0.7, 0.2, 0.1])
}

df = pd.DataFrame(data)

# Sauvegarder
os.makedirs('/app/datasets/CICIDS2017', exist_ok=True)
df.to_csv('/app/datasets/CICIDS2017/Monday-WorkingHours.pcap_ISCX.csv', index=False)

print(f"✅ Synthetic dataset created: {len(df)} samples")
print(f"   BENIGN: {(df['Label']=='BENIGN').sum()}")
print(f"   DDoS: {(df['Label']=='DDoS').sum()}")
print(f"   PortScan: {(df['Label']=='PortScan').sum()}")