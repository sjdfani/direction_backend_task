from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import automatic_extract_jobs


class ExtractJobs(APIView):
    def get(self, request):
        automatic_extract_jobs.delay()
        message = {"message": "Job extraction started"}
        return Response(message, status=status.HTTP_200_OK)
