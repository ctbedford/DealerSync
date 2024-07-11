from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import run_scrapers
from .models import SyncAttempt, VehicleListing
from celery.result import AsyncResult
from django.utils import timezone
from celery.exceptions import OperationalError
from .serializers import VehicleListingSerializer

class DumpListingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        listings = VehicleListing.objects.filter(user=request.user)
        serializer = VehicleListingSerializer(listings, many=True)
        return Response({
            "count": listings.count(),
            "listings": serializer.data
        })


class StartScraperView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            task = run_scrapers.delay()
            return Response({"message": "Scraper task started", "task_id": str(task.id)})
        except OperationalError:
            return Response({"error": "Could not connect to task queue. Please try again later."}, status=503)

class ScraperStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({"error": "No task_id provided"}, status=400)

        try:
            task_result = AsyncResult(task_id)
            if task_result.state == 'PENDING':
                response = {
                    'state': task_result.state,
                    'status': 'Sync task is pending...'
                }
            elif task_result.state != 'FAILURE':
                response = {
                    'state': task_result.state,
                    'status': str(task_result.info),
                }
            else:
                response = {
                    'state': task_result.state,
                    'status': str(task_result.info),
                }
            return Response(response)
        except OperationalError:
            return Response({"error": "Could not connect to task queue. Please try again later."}, status=503)
            
class RunScraperNowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        sync_attempt = SyncAttempt.objects.create(user=user, status='IN_PROGRESS')
        try:
            task = run_scrapers.delay(user.id)
            return Response({
                "message": "Scraper started",
                "sync_attempt_id": sync_attempt.id,
                "task_id": str(task.id)
            })
        except Exception as e:
            sync_attempt.status = 'FAILED'
            sync_attempt.error_message = str(e)
            sync_attempt.save()
            return Response({"error": str(e)}, status=500)


        
class SyncHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        last_successful = SyncAttempt.objects.filter(user=user, status='COMPLETED').order_by('-end_time').first()
        sync_history = {
            "lastSuccessful": last_successful.end_time.isoformat() if last_successful else None,
            "totalToday": SyncAttempt.objects.filter(user=user, start_time__date=today).count(),
            "failedToday": SyncAttempt.objects.filter(user=user, start_time__date=today, status='FAILED').count()
        }
        return Response(sync_history)