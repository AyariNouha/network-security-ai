from scapy.all import sniff, IP, TCP, UDP, ICMP
from .models import NetworkFlow
import time

def process_packet(packet):
    """Traiter un packet capturé"""
    try:
        if IP in packet:
            # Extraire infos
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Déterminer protocole et ports
            if TCP in packet:
                protocol = 'TCP'
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
            elif UDP in packet:
                protocol = 'UDP'
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
            elif ICMP in packet:
                protocol = 'ICMP'
                src_port = 0
                dst_port = 0
            else:
                protocol = 'OTHER'
                src_port = 0
                dst_port = 0
            
            # Créer NetworkFlow
            flow = NetworkFlow.objects.create(
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_port=src_port,
                dst_port=dst_port,
                protocol=protocol,
                packet_size=len(packet),
                flow_duration=0.0
            )
            
            return flow.id
            
    except Exception as e:
        print(f"❌ Error processing packet: {e}")
        return None

def start_capture(interface='any', count=50, timeout=30):
    """Capturer des packets"""
    print(f"🔍 Starting packet capture...")
    print(f"   Interface: {interface}")
    print(f"   Count: {count}")
    print(f"   Timeout: {timeout}s")
    
    try:
        packets = sniff(
            iface=interface,
            prn=process_packet,
            count=count,
            timeout=timeout,
            store=False
        )
        print(f"✅ Captured packets")
        return count
    except Exception as e:
        print(f"❌ Capture error: {e}")
        return 0