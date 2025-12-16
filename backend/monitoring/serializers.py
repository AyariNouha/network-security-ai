from rest_framework import serializers
from .models import NetworkFlow, Alert

class NetworkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkFlow
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'