from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from scraper.tasks import run_scrapers
from scraper.models import VehicleListing, SyncAttempt
from .serializers import VehicleListingSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_listings = VehicleListing.objects.filter(user=user).count()
        today = timezone.now().date()
        listings_today = VehicleListing.objects.filter(user=user, created_at__date=today).count()
        
        active_syncs = SyncAttempt.objects.filter(user=user, status='IN_PROGRESS').count()
        pending_updates = VehicleListing.objects.filter(user=user, needs_update=True).count()
        total_views = VehicleListing.objects.filter(user=user).aggregate(total_views=Count('views'))['total_views']

        # Get data for chart (last 4 months)
        chart_data = []
        for i in range(3, -1, -1):
            month_start = (timezone.now() - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            listings_count = VehicleListing.objects.filter(user=user, created_at__range=(month_start, month_end)).count()
            views_count = VehicleListing.objects.filter(user=user, created_at__range=(month_start, month_end)).aggregate(total_views=Count('views'))['total_views']
            chart_data.append({
                "name": month_start.strftime("%b"),
                "listings": listings_count,
                "views": views_count
            })

        # Recent activity (last 4 events)
        recent_listings = VehicleListing.objects.filter(user=user).order_by('-created_at')[:4]
        recent_activity = [
            {
                "title": "New Listing Added",
                "description": f"{listing.year} {listing.make} {listing.model}",
                "time": f"{(timezone.now() - listing.created_at).days} days ago"
            } for listing in recent_listings
        ]

        dashboard_data = {
            "stats": [
                {"title": "Total Listings", "value": total_listings, "icon": "Car"},
                {"title": "Active Syncs", "value": active_syncs, "icon": "Activity"},
                {"title": "Pending Updates", "value": pending_updates, "icon": "Clock"},
                {"title": "Total Views", "value": total_views, "icon": "Eye"},
            ],
            "recentActivity": recent_activity,
            "chartData": chart_data
        }
        return Response(dashboard_data)


class ListingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 20
        listings = VehicleListing.objects.filter(user=request.user).order_by('-created_at')
        result_page = paginator.paginate_queryset(listings, request)
        serializer = VehicleListingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class SyncHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        last_successful = SyncAttempt.objects.filter(status='COMPLETED').order_by('-end_time').first()
        sync_history = {
            "lastSuccessful": last_successful.end_time if last_successful else None,
            "totalToday": SyncAttempt.objects.filter(start_time__date=today).count(),
            "failedToday": SyncAttempt.objects.filter(start_time__date=today, status='FAILED').count()
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