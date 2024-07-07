from django.urls import path
from .views import StartScraperView, ScraperStatusView, RunScraperNowView, SyncHistoryView, DumpListingsView

urlpatterns = [
    path('start/', StartScraperView.as_view(), name='start_scraper'),
    path('status/', ScraperStatusView.as_view(), name='scraper_status'),
    path('run-now/', RunScraperNowView.as_view(), name='run_scraper_now'),
    path('sync/history/', SyncHistoryView.as_view(), name='sync_history'),
    path('dump-listings/', DumpListingsView.as_view(), name='dump_listings'),
]
