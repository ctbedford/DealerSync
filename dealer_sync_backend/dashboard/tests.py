from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from scraper.models import VehicleListing, SyncAttempt
from django.utils import timezone

class DashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        # Create some test data
        VehicleListing.objects.create(
            dealership="Test Dealer",
            title="2023 Test Car",
            price=25000,
            msrp=26000,
            year=2023,
            make="Test",
            model="Car"
        )
        SyncAttempt.objects.create(status='COMPLETED')

    def test_dashboard_data(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stats', response.data)
        self.assertIn('recentActivity', response.data)
        self.assertIn('chartData', response.data)

    def test_listings_view(self):
        url = reverse('listings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_sync_history_view(self):
        url = reverse('sync_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('lastSuccessful', response.data)
        self.assertIn('totalToday', response.data)
        self.assertIn('failedToday', response.data)