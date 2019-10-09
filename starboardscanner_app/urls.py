from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet)
router.register(r'records', views.RecordViewSet)

urlpatterns = [
    path('', views.home, name='starboardscanner_app-home'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
