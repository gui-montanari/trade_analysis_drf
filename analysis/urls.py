from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('futures/', views.futures_analysis, name='futures'),
    path('futures/refresh/', views.refresh_futures, name='refresh_futures'),
]