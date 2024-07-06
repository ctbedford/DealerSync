from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import run_scrapers

class StartScraperView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        task = run_scrapers.delay()
        return Response({"message": "Scraper task started", "task_id": str(task.id)})