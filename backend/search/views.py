import os

import requests
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.search.serializers import SearchRequestSerializer


@extend_schema(
    summary="Search in GitHub",
    description="Search GitHub repositories, users or issues.",
    tags=["search"],
    request=SearchRequestSerializer,
    responses={
        200: "Success", 400: "Invalid input", 502: "GitHub error"
    },
)
class GitHubSearchView(APIView):

    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_type = serializer.validated_data['type']
        query = serializer.validated_data['query']

        cache_key = f"{search_type}:{query}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)

        # Auth https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28#authentication
        url = f"{os.getenv("GITHUB_LINK")}{search_type}?q={query}&per_page=10&page=1"
        headers = {"Accept": "application/vnd.github+json"}


        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        data = response.json()
        cache.set(cache_key, data, timeout=60 * 60 * 2)  # 2 hours
        return Response(data)


class ClearCacheView(APIView):
    def post(self, request):
        cache.clear()
        return Response({"message": "Cache cleared."}, status=status.HTTP_200_OK)
