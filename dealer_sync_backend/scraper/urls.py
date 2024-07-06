from django.urls import path
from .views import StartScraperView

urlpatterns = [
    path('start/', StartScraperView.as_view(), name='start_scraper'),
]