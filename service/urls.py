from django.urls import path
from . import views

urlpatterns = [
    # Vehicle Endpoints
    path('vehicles/', views.get_vehicles, name='get_vehicles'),
    path('vehicles/create/', views.create_vehicle, name='create_vehicle'),

    # Component Endpoints
    path('components/', views.get_components, name='get_components'),
    path('components/create/', views.create_component, name='create_component'),

    # Service Issues Endpoints
    path('service-issues/', views.get_service_issues, name='get_service_issues'),
    path('service-issues/create/', views.create_service_issue, name='create_service_issue'),


    path('analytics/data/', views.analytics_data, name='analytics_data'),
]
