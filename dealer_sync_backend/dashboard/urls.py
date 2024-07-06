

from django.urls import path
from .views import DashboardView, ListingsView, SyncHistoryView, SyncStartView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('listings/', ListingsView.as_view(), name='listings'),
    path('sync/history/', SyncHistoryView.as_view(), name='sync_history'),
    path('sync/start/', SyncStartView.as_view(), name='sync_start'),
]
