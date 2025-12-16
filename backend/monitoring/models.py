from django.db import models

class NetworkFlow(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    src_ip = models.GenericIPAddressField()
    dst_ip = models.GenericIPAddressField()
    src_port = models.IntegerField()
    dst_port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    packet_size = models.IntegerField()
    flow_duration = models.FloatField(default=0)
    is_anomaly = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.src_ip}:{self.src_port} -> {self.dst_ip}:{self.dst_port}"

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    TYPE_CHOICES = [
        ('ML', 'Machine Learning'),
        ('Signature', 'Signature-based'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    src_ip = models.GenericIPAddressField()
    dst_ip = models.GenericIPAddressField()
    confidence_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"[{self.severity}] {self.alert_type} - {self.description[:50]}"