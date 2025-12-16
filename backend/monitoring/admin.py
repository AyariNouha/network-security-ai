from django.contrib import admin
from .models import NetworkFlow, Alert

@admin.register(NetworkFlow)
class NetworkFlowAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'src_ip', 'dst_ip', 'protocol', 'packet_size', 'is_anomaly']
    list_filter = ['protocol', 'is_anomaly', 'timestamp']
    search_fields = ['src_ip', 'dst_ip']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'alert_type', 'severity', 'src_ip', 'dst_ip', 'description']
    list_filter = ['alert_type', 'severity', 'timestamp']
    search_fields = ['src_ip', 'dst_ip', 'description']