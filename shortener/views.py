from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer
from django.shortcuts import redirect, get_object_or_404
import logging
import json
import redis
from django.core.cache import cache  # Import the cache framework
# print("shortener/views.py is being loaded...")
logger = logging.getLogger(__name__)
class URLViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating short URLs.
    """
    def __init__(self, *args, **kwargs):
        # print("URLViewSet is initialized")
        super().__init__(*args, **kwargs)
    # print("In View")
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        # print("Create view was reached")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Include redirect_count in the response
        # print([i for i in serializer.data])
        logger.info(json.dumps(serializer.data))  # Log as JSON string
        # response_data = {**serializer.data, 'redirect_count': 0}
        # print(f"Created URL entry: {response_data}")
        short_code = serializer.data['short_code']
        original_url = serializer.data['original_url']
        cache.set(short_code, original_url, timeout=3600)  # Cache on creation
        return Response({**serializer.data, 'redirect_count': 0}, status=status.HTTP_201_CREATED, headers=headers)

def pstate(request):
    print("Called !")



@api_view(['GET'])
def redirect_view(request, short_code):
    """
    Redirects short URLs to their original URLs.
    """
    original_url = cache.get(short_code)
    if original_url:
        return redirect(original_url)
    url_obj = get_object_or_404(URL, short_code=short_code)
    original_url_db = url_obj.original_url

    url_obj.redirect_count += 1
    url_obj.save()

    cache.set(short_code, original_url_db, timeout=3600)
    # print("Cache: "+cache.get(short_code))
    return redirect(original_url_db)
    # try:
    #     url = URL.objects.get(short_code=short_code)
    #     url.redirect_count += 1
    #     url.save()
    #     return redirect(url.original_url)
    # except URL.DoesNotExist:
    #     return Response({'error': 'Short URL not found'}, status=status.HTTP_404_NOT_FOUND)