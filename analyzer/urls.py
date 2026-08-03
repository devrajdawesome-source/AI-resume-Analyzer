from django.urls import path
from .views import HealthCheckView, AnalyzeResumeView, AnalysisHistoryView, home_view, RegisterView

urlpatterns = [
    path('', home_view, name='home'),
    path('api/health/', HealthCheckView.as_view(), name='health_check'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/analyze/', AnalyzeResumeView.as_view(), name='analyze_resume'),
    path('api/history/', AnalysisHistoryView.as_view(), name='analysis_history'),
]