from django.urls import path
from .views import ExtractJobs

app_name = "job"

urlpatterns = [
    path("extract/", ExtractJobs.as_view(), name="ExtractJobs"),
]
