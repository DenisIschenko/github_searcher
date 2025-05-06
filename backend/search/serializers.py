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
