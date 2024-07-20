from django.urls import path
from .views import StartScraperView, ScraperStatusView, SyncHistoryView, DumpListingsView, DashboardView

urlpatterns = [
    path('start/', StartScraperView.as_view(), name='start-scraper'),
    path('status/', ScraperStatusView.as_view(), name='scraper-status'),
    path('sync/history/', SyncHistoryView.as_view(), name='sync-history'),
    path('listings/', DumpListingsView.as_view(), name='dump-listings'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('run-now/', StartScraperView.as_view(), name='run-scraper'),

]
