from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class SearchRequestSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["users", "repositories", "issues"], error_messages={
        'required': _("Field 'Type' is required."),
        'null': _("Field 'Type' may not be null.")
    })
    query = serializers.CharField(error_messages={
        'required': _("Field 'Query' is required."),
        'null': _("Field 'Query' may not be null.")
    })


class SearchUserResponseSerializer(serializers.Serializer):
    avatar_url = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    login = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    html_url = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    name = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    company = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    location = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    email = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    bio = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    public_repos = serializers.IntegerField(required=False, default=0, allow_null=True)
    followers = serializers.IntegerField(required=False, default=0, allow_null=True)
    following = serializers.IntegerField(required=False, default=0, allow_null=True)
    type = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    node_id = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    id = serializers.IntegerField()


class SearchRepositoryResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    node_id = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    name = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    full_name = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    owner = SearchUserResponseSerializer()
    private = serializers.BooleanField(default=False)
    html_url = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    description = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    fork = serializers.BooleanField(default=False)
    forks_count = serializers.IntegerField(default=0)
    forks = serializers.IntegerField(default=0)
    stargazers_count = serializers.IntegerField(default=0)
    watchers_count = serializers.IntegerField(default=0)
    watchers = serializers.IntegerField(default=0)
    size = serializers.IntegerField(default=0)
    default_branch = serializers.CharField(required=False, default='', allow_blank=True, allow_null=True)
    open_issues_count = serializers.IntegerField(default=0)
    open_issues = serializers.IntegerField(default=0)
    subscribers_count = serializers.IntegerField(default=0)
    network_count = serializers.IntegerField(default=0)
    license = serializers.DictField(required=False, allow_null=True, default={})
