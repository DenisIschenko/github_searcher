import os

import requests
from django.conf import settings
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search.serializers import SearchRequestSerializer, SearchUserResponseSerializer, SearchRepositoryResponseSerializer

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}"
}


@extend_schema(
    summary="Search in GitHub",
    description="Search GitHub repositories, users or issues.",
    tags=["search"],
    request=SearchRequestSerializer,
    responses={
        200: PolymorphicProxySerializer(
            component_name="SearchResponseSerializer",
            serializers=[SearchUserResponseSerializer, SearchRepositoryResponseSerializer],
            resource_type_field_name=None,
        ), 400: "Invalid input", 502: "GitHub error"
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

        url = f"{os.getenv("GITHUB_LINK")}{search_type}?q={query}&per_page=12&page=1"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            serialized_data = self.__process_search_data(response.json(), search_type)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        if response.status_code == 200:
            cache.set(cache_key, serialized_data, timeout=settings.GITHUB_SEARCH_CACHE_TIMEOUT)
        return Response(serialized_data)

    def __process_search_data(self, data, search_type):
        data = data.get("items", [])
        full_data = []
        serializer = None

        for item in data:
            item_data = self.__load_data(item, search_type)
            if search_type == "repositories":
                item_data['owner'] = self.__load_data(item.get('owner', {}), "users")

            full_data.append(item_data)

        if search_type == "repositories":
            serializer = SearchRepositoryResponseSerializer(data=full_data, many=True)
            serializer.is_valid(raise_exception=True)
        elif search_type == "users":
            serializer = SearchUserResponseSerializer(data=full_data, many=True)
            serializer.is_valid(raise_exception=True)
        else:
            pass

        return serializer.validated_data

    def __load_data(self, item, search_type):
        # Load data into the cache
        cache_key = f"{search_type}:{item.get('id')}"
        item_data = cache.get(cache_key)
        if not item_data:
            response = requests.get(item.get('url'), headers=headers, timeout=10)
            response.raise_for_status()
            item_data = response.json()
            cache.set(cache_key, item_data, timeout=settings.GITHUB_SEARCH_CACHE_TIMEOUT)

        return item_data


class ClearCacheView(APIView):
    def post(self, request):
        cache.clear()
        return Response({"message": "Cache cleared."}, status=status.HTTP_200_OK)
