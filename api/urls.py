# taskmanager/urls.py

from django.urls import path
from .views import start_scraping

urlpatterns = [
    path("api/taskmanager/start_scraping", start_scraping),
]
