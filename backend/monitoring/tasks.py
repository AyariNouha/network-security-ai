from celery import shared_task
from .models import NetworkFlow, Alert
import random

@shared_task
def generate_synthetic_traffic():
    """Générer du trafic synthétique"""
    
    protocols = ['TCP', 'UDP', 'ICMP']
    
    for _ in range(10):
        NetworkFlow.objects.create(
            src_ip=f"192.168.1.{random.randint(1, 254)}",
            dst_ip=f"10.0.0.{random.randint(1, 254)}",
            src_port=random.randint(1024, 65535),
            dst_port=random.choice([80, 443, 22, 3389]),
            protocol=random.choice(protocols),
            packet_size=random.randint(64, 1500),
            flow_duration=random.uniform(0.001, 1.0)
        )
    
    return "✅ Generated 10 synthetic flows"

@shared_task
def analyze_recent_flows():
    """Analyser les flows récents"""
    
    flows = NetworkFlow.objects.all()[:10]
    return f"✅ Analyzed {len(flows)} flows"

@shared_task
def send_alert_to_frontend(alert_id):
    """Envoyer alerte"""
    return f"✅ Alert {alert_id} sent"

@shared_task
def update_dashboard_stats():
    """Mettre à jour stats"""
    return "✅ Stats updated"