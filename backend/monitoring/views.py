from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import NetworkFlow, Alert
from .serializers import NetworkFlowSerializer, AlertSerializer
from datetime import timedelta
from django.utils import timezone

class NetworkFlowViewSet(viewsets.ModelViewSet):
    queryset = NetworkFlow.objects.all()
    serializer_class = NetworkFlowSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

@api_view(['GET'])
def dashboard_stats(request):
    """Stats pour dashboard"""
    total_flows = NetworkFlow.objects.count()
    total_alerts = Alert.objects.count()
    anomalies = NetworkFlow.objects.filter(is_anomaly=True).count()
    
    # Stats par protocole
    protocol_stats = NetworkFlow.objects.values('protocol').annotate(
        count=Count('id')
    )
    
    # Alertes par sévérité
    severity_stats = Alert.objects.values('severity').annotate(
        count=Count('id')
    )
    
    # Taux de détection
    detection_rate = (anomalies / total_flows * 100) if total_flows > 0 else 0
    
    return Response({
        'total_flows': total_flows,
        'total_alerts': total_alerts,
        'anomalies': anomalies,
        'detection_rate': round(detection_rate, 2),
        'protocol_distribution': list(protocol_stats),
        'severity_distribution': list(severity_stats)
    })

@api_view(['GET'])
def traffic_timeline(request):
    """Timeline du trafic (24h)"""
    last_24h = timezone.now() - timedelta(hours=24)
    flows = NetworkFlow.objects.filter(timestamp__gte=last_24h)
    
    timeline = []
    for hour in range(24):
        hour_start = last_24h + timedelta(hours=hour)
        hour_end = hour_start + timedelta(hours=1)
        count = flows.filter(
            timestamp__gte=hour_start,
            timestamp__lt=hour_end
        ).count()
        timeline.append({
            'hour': hour_start.strftime('%H:%M'),
            'count': count
        })
    
    return Response(timeline)

@api_view(['GET'])
def top_talkers(request):
    """Top IPs avec le plus de trafic"""
    top_src = NetworkFlow.objects.values('src_ip').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    top_dst = NetworkFlow.objects.values('dst_ip').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    return Response({
        'top_sources': list(top_src),
        'top_destinations': list(top_dst)
    })