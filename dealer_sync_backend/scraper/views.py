from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import run_scrapers
from .scraper import scrape_mclarty_daniel
from celery.result import AsyncResult

class StartScraperView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        task = run_scrapers.delay()
        return Response({"message": "Scraper task started", "task_id": str(task.id)})

class ScraperStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({"error": "No task_id provided"}, status=400)

        task_result = AsyncResult(task_id)
        return Response({
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result
        })

class RunScraperNowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            scrape_mclarty_daniel()
            return Response({"message": "Scraper ran successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
