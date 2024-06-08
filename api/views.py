# from django.shortcuts import render
"""from rest_framework import generics
from .models import Data
from .serializers import Data_Serializer


class Data_list(generics.ListCreateAPIView): 
    serializer_class = Data_Serializer

    def get_queryset(self):
        queryset = Data.objects.all()
        return queryset


# Create your views here."""
# taskmanager/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main import run

@api_view(['POST'])
def start_scraping(request):
    if not isinstance(request.data, list):
        return Response({"error": "Invalid payload format, expected a list."}, status=status.HTTP_400_BAD_REQUEST)
    
    crypto_list = request.data
    print(crypto_list)
    scraped_data = run(crypto_list)
    return Response(scraped_data, status=status.HTTP_200_OK)

