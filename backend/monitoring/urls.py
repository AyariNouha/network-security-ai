from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'flows', views.NetworkFlowViewSet)
router.register(r'alerts', views.AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.dashboard_stats, name='stats'),
    path('timeline/', views.traffic_timeline, name='timeline'),
    path('top-talkers/', views.top_talkers, name='top-talkers'),
]