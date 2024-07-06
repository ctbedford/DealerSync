from django.urls import path
from .views import StartScraperView, ScraperStatusView, RunScraperNowView

urlpatterns = [
    path('start/', StartScraperView.as_view(), name='start_scraper'),
    path('status/', ScraperStatusView.as_view(), name='scraper_status'),
    path('run-now/', RunScraperNowView.as_view(), name='run_scraper_now'),
]

