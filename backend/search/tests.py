from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from django.core.cache import cache
from requests.exceptions import RequestException

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
        self.url_clean = reverse("clear-cache")
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
        # self.client.post(self.url_clean)
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
