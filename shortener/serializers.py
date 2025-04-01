from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_code', 'created_at', 'redirect_count', 'short_url']
        read_only_fields = ['id', 'short_code', 'created_at', 'redirect_count']

    def get_short_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/{obj.short_code}')