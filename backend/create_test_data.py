import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from monitoring.models import NetworkFlow, Alert
import random

# Créer 50 flows
for i in range(50):
    NetworkFlow.objects.create(
        src_ip=f"192.168.1.{random.randint(1, 254)}",
        dst_ip=f"10.0.0.{random.randint(1, 254)}",
        src_port=random.randint(1024, 65535),
        dst_port=random.choice([80, 443, 22, 3389]),
        protocol=random.choice(['TCP', 'UDP', 'ICMP']),
        packet_size=random.randint(64, 1500),
        is_anomaly=random.choice([True, False])
    )

# Créer 10 alertes
for i in range(10):
    Alert.objects.create(
        alert_type=random.choice(['ML', 'Signature']),
        severity=random.choice(['HIGH', 'MEDIUM', 'LOW']),
        description=f"Test alert {i}",
        src_ip=f"192.168.1.{random.randint(1, 254)}",
        dst_ip=f"10.0.0.{random.randint(1, 254)}",
        confidence_score=random.uniform(0.5, 0.99)
    )

print("✅ Test data created!")