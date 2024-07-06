from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from scraper.tasks import run_scrapers

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dashboard_data = {
            "stats": [
                {"title": "Total Listings", "value": 150, "icon": "Car"},
                {"title": "Active Syncs", "value": 3, "icon": "Activity"},
                {"title": "Pending Updates", "value": 10, "icon": "Clock"},
                {"title": "Total Views", "value": 1250, "icon": "Eye"},
            ],
            "recentActivity": [
                {"title": "New Listing Added", "description": "2023 Toyota Camry", "time": "2 hours ago"},
                {"title": "Sync Completed", "description": "Marketplace A", "time": "4 hours ago"},
                {"title": "Price Updated", "description": "5 listings", "time": "1 day ago"},
                {"title": "New Inquiry", "description": "Regarding 2022 Honda Civic", "time": "2 days ago"},
            ],
            "chartData": [
                {"name": "Jan", "listings": 120, "views": 1000},
                {"name": "Feb", "listings": 135, "views": 1100},
                {"name": "Mar", "listings": 142, "views": 1200},
                {"name": "Apr", "listings": 150, "views": 1250},
            ]
        }
        return Response(dashboard_data)

class ListingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        listings_data = [
            {"id": 1, "make": "Toyota", "model": "Camry", "year": 2023, "price": 25000, "status": "Active"},
            {"id": 2, "make": "Honda", "model": "Civic", "year": 2022, "price": 22000, "status": "Pending"},
            {"id": 3, "make": "Ford", "model": "F-150", "year": 2023, "price": 35000, "status": "Active"},
            {"id": 4, "make": "Chevrolet", "model": "Malibu", "year": 2022, "price": 23000, "status": "Inactive"},
        ]
        return Response(listings_data)

class SyncHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sync_history = {
            "lastSuccessful": "2 hours ago",
            "totalToday": 5,
            "failedToday": 0
        }
        return Response(sync_history)


class SyncStartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Trigger the Celery task
        task = run_scrapers.delay()
        return Response({
            "message": "Sync process started",
            "task_id": task.id
        })