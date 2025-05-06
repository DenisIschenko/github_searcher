from django.urls import path
from .views import GitHubSearchView, ClearCacheView

urlpatterns = [
    path('search', GitHubSearchView.as_view(), name='github-search'),
    path('clear-cache', ClearCacheView.as_view(), name='clear-cache'),
]