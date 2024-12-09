from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    # Futures Trading
    path('futures/', views.futures_analysis, name='futures'),
    path('futures/refresh/', views.refresh_futures, name='refresh_futures'),
    
    # Day Trading
    path('daytrading/', views.day_trading_analysis, name='daytrading'),
    path('daytrading/refresh/', views.refresh_daytrading, name='refresh_daytrading'),
    
    # Swing Trading
    path('swing/', views.swing_analysis, name='swing'),
    path('swing/refresh/', views.refresh_swing, name='refresh_swing'),
    
    # Position Trading
    path('position/', views.position_analysis, name='position'),
    path('position/refresh/', views.refresh_position, name='refresh_position'),
]