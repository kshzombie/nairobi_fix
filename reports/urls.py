from django.urls import path
from . import views


urlpatterns = [
    # Pages
    path('', views.dashboard, name='dashboard'),
    path('report/', views.report_issue, name='report_issue'),
    path('streetlight-report/', views.streetlight_report_issue, name='streetlight_report_issue'),
    path('success/', views.report_success, name='report_success'),

    # API Data Endpoints
    path('api/potholes/', views.pothole_data, name='pothole_data'),
    path('api/streetlights/', views.streetlight_data, name='streetlight_data'),
    path('api/subcounties/', views.subcounty_data, name='subcounty_data'),
]
