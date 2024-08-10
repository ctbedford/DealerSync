from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .tasks import run_scrapers
from .models import SyncAttempt, VehicleListing
from celery.result import AsyncResult
from django.utils import timezone
from celery.exceptions import OperationalError
from .serializers import VehicleListingSerializer
from django.core.exceptions import FieldError
from django.db.models import Count
from typing import List
import logging

logger = logging.getLogger(__name__)


class StartScraperView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logger.info(f"Starting scraper task for user {request.user.id}")
            task = run_scrapers.delay(request.user.id)
            sync_attempt = SyncAttempt.objects.create(
                user=request.user,
                task_id=task.id,
                status='PENDING'
            )
            logger.info(f"Scraper task started. Task ID: {task.id}")
            return Response({"message": "Scraper task started", "task_id": str(task.id)})
        except OperationalError as e:
            logger.error(f"OperationalError while starting scraper: {str(e)}")
            return Response({"error": "Could not connect to task queue. Please try again later."}, status=503)
        except Exception as e:
            logger.exception(
                f"Unexpected error while starting scraper: {str(e)}")
            return Response({"error": "An unexpected error occurred. Please try again."}, status=500)


class ScraperStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_id = request.query_params.get('task_id')
        user_id = request.user.id
        logger.info(f"Checking scraper status. Task ID: {
                    task_id}, User ID: {user_id}")

        if not task_id:
            logger.warning("No task_id provided in request")
            return Response({"error": "No task_id provided"}, status=400)

        try:
            sync_attempt = SyncAttempt.objects.filter(
                task_id=task_id, user_id=user_id).first()
            if not sync_attempt:
                logger.warning(f"No sync attempt found for task {
                               task_id} and user {user_id}")
                return Response({"error": "No sync attempt found for this task and user"}, status=404)

            task_result = AsyncResult(task_id)
            logger.info(f"Task state: {task_result.state}")

            response = {
                'state': task_result.state,
                'userId': user_id,
            }

            if task_result.state == 'PENDING':
                response['status'] = 'Sync task is pending...'
            elif task_result.state == 'PROGRESS':
                info = task_result.info or {}
                response.update({
                    'current': info.get('current', 0),
                    'total': info.get('total', 'unknown'),
                    'percent': info.get('percent', 0),
                    'status': f"Processing vehicle {info.get('current', 0)} of {info.get('total', 'unknown')}",
                    'currentVehicle': info.get('currentVehicle', 'Unknown'),
                })
                logger.info(f"Returning progress response: {response}")
            elif task_result.state == 'SUCCESS':
                response['status'] = task_result.result
            else:
                response['status'] = str(task_result.info)

            logger.info(f"Returning response for task {task_id}: {response}")
            return Response(response)
        except Exception as e:
            logger.exception(
                f"Unexpected error while checking scraper status: {str(e)}")
            return Response({"error": "An unexpected error occurred. Please try again."}, status=500)


class DumpListingsView(APIView):
    permission_classes: List[type[BasePermission]] = [IsAuthenticated]

    def get(self, request):
        try:
            logger.info(f"Fetching listings for user {request.user.id}")
            listings = VehicleListing.objects.filter(user=request.user)
            serializer = VehicleListingSerializer(listings, many=True)
            logger.info(f"Retrieved {listings.count()
                                     } listings for user {request.user.id}")
            return Response({
                "count": listings.count(),
                "listings": serializer.data
            })
        except FieldError as e:
            logger.error(f"FieldError while fetching listings: {str(e)}")
            return Response({"error": f"FieldError: {str(e)}"}, status=400)
        except Exception as e:
            logger.exception(
                f"Unexpected error while fetching listings: {str(e)}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


class SyncHistoryView(APIView):
    permission_classes: List[type[BasePermission]] = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        logger.info(f"Fetching sync history for user {user.id}")

        try:
            last_successful = SyncAttempt.objects.filter(
                user=user, status='COMPLETED').order_by('-end_time').first()
            sync_history = {
                "lastSuccessful": last_successful.end_time.isoformat() if last_successful else None,
                "totalToday": SyncAttempt.objects.filter(user=user, start_time__date=today).count(),
                "failedToday": SyncAttempt.objects.filter(user=user, start_time__date=today, status='FAILED').count()
            }
            logger.info(f"Sync history for user {user.id}: {sync_history}")
            return Response(sync_history)
        except Exception as e:
            logger.exception(f"Error fetching sync history for user {
                             user.id}: {str(e)}")
            return Response({"error": "Failed to fetch sync history"}, status=500)


class DashboardView(APIView):
    permission_classes: List[type[BasePermission]] = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"Fetching dashboard data for user {user.id}")

        try:
            total_listings = VehicleListing.objects.filter(user=user).count()
            today = timezone.now().date()
            listings_today = VehicleListing.objects.filter(
                user=user, created_at__date=today).count()

            active_syncs = SyncAttempt.objects.filter(
                user=user, status='IN_PROGRESS').count()
            pending_updates = VehicleListing.objects.filter(
                user=user, needs_update=True).count()
            total_views = VehicleListing.objects.filter(user=user).aggregate(
                total_views=Count('views'))['total_views']

            # Get data for chart (last 4 months)
            chart_data = []
            for i in range(3, -1, -1):
                month_start = (timezone.now() -
                               timezone.timedelta(days=30*i)).replace(day=1)
                month_end = (month_start + timezone.timedelta(days=32)
                             ).replace(day=1) - timezone.timedelta(days=1)
                listings_count = VehicleListing.objects.filter(
                    user=user, created_at__range=(month_start, month_end)).count()
                views_count = VehicleListing.objects.filter(user=user, created_at__range=(
                    month_start, month_end)).aggregate(total_views=Count('views'))['total_views']
                chart_data.append({
                    "name": month_start.strftime("%b"),
                    "listings": listings_count,
                    "views": views_count
                })

            # Recent activity (last 4 events)
            recent_listings = VehicleListing.objects.filter(
                user=user).order_by('-created_at')[:4]
            recent_activity = [
                {
                    "title": "New Listing Added",
                    "description": f"{listing.year} {listing.make} {listing.model}",
                    "time": f"{(timezone.now() - listing.created_at).days} days ago"
                } for listing in recent_listings
            ]

            dashboard_data = {
                "stats": [
                    {"title": "Total Listings",
                        "value": total_listings, "icon": "Car"},
                    {"title": "Active Syncs",
                        "value": active_syncs, "icon": "Activity"},
                    {"title": "Pending Updates",
                        "value": pending_updates, "icon": "Clock"},
                    {"title": "Total Views", "value": total_views, "icon": "Eye"},
                ],
                "recentActivity": recent_activity,
                "chartData": chart_data
            }
            logger.info(
                f"Dashboard data fetched successfully for user {user.id}")
            return Response(dashboard_data)
        except Exception as e:
            logger.exception(f"Error fetching dashboard data for user {
                             user.id}: {str(e)}")
            return Response({"error": "Failed to fetch dashboard data"}, status=500)
