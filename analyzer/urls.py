from django.urls import path
from .views import HealthCheckView, AnalyzeResumeView, AnalysisHistoryView, home_view

urlpatterns = [
    # Homepage UI
    path('', home_view, name='home'),
    
    # API Endpoints
    path('api/health/', HealthCheckView.as_view(), name='health_check'),
    path('api/analyze/', AnalyzeResumeView.as_view(), name='analyze_resume'),
    path('api/history/', AnalysisHistoryView.as_view(), name='analysis_history'),
]