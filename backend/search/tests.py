import time
from unittest.mock import patch, MagicMock

from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from search.serializers import SearchRequestSerializer


class SearchRequestSerializerTest(APITestCase):
    def test_valid_serializer(self):
        data = {"type": "users", "query": "john"}
        serializer = SearchRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_missing_field(self):
        data = {"type": "users"}
        serializer = SearchRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_serializer_wrong_type(self):
        data = {"type": "invalid", "query": "test"}
        serializer = SearchRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class GitHubSearchViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("github-search")
        cache.clear()

    @patch("search.views.requests.get")
    def test_successful_search(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"items": [{"id": 1, "name": "test"}]}

        response = self.client.post(self.url, {"type": "users", "query": "john"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)

    @patch("search.views.requests.get")
    def test_github_api_failure(self, mock_get):
        mock_get.side_effect = RequestException("GitHub is down")

        response = self.client.post(self.url, {"type": "users", "query": "john"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_invalid_input(self):
        response = self.client.post(self.url, {"type": "invalid", "query": "test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("search.views.requests.get")
    def test_cached_response(self, mock_get):
        cache.set("users:john", {"items": [{"id": 99}]})

        response = self.client.post(self.url, {"type": "users", "query": "john"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"][0]["id"], 99)
        mock_get.assert_not_called()


ttl = 2  # seconds


class CacheTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("github-search")
        cache.clear()

    @override_settings(GITHUB_SEARCH_CACHE_TIMEOUT=ttl)
    @patch("search.views.requests.get")
    def test_cache_ttl_expiry(self, mock_get):
        cache_key = "users:john"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"items": [{"id": 1, "login": "john"}]}

        # Cache the response
        response = self.client.post(self.url, {"type": "users", "query": "john"}, format="json")
        self.assertEqual(response.status_code, 200)

        # Check if the cache is set
        self.assertIsNotNone(cache.get(cache_key))

        # Wait while the cache expires
        time.sleep(ttl + 1)

        # Cache should be expired
        self.assertIsNone(cache.get(cache_key))

    @patch("search.views.requests.get")
    def test_response_is_cached_only_on_200(self, mock_get):
        cache_key = "users:john"

        # --- Case: 500 --- #
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server error"}
        mock_get.return_value = mock_response

        response = self.client.post(self.url, {"type": "users", "query": "john"}, format="json")
        self.assertEqual(response.status_code, 500)
        self.assertIsNone(cache.get(cache_key), msg="Cache should not be created on 500 error")

        cache.clear()

        # --- Case: 200 --- #
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": 1, "login": "john"}]}

        response = self.client.post(self.url, {"type": "users", "query": "john"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(cache.get(cache_key), msg="Cache should be created on 200 response")