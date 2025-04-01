from django.db import models

# Create your models here.
from django.db import models
import shortuuid
from django.utils import timezone

class URL(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=shortuuid.uuid)
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=8, unique=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    redirect_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = shortuuid.uuid()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.short_code} -> {self.original_url}'