from django.contrib import admin

# Register your models here.
from .models import URL
from django.contrib import admin
from .models import URL
class URLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'created_at', 'redirect_count')
    search_fields = ('short_code', 'original_url')
    list_filter = ('created_at',)
admin.site.register(URL, URLAdmin)