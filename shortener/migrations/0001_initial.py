# Generated by Django 4.2.20 on 2025-03-14 21:52

from django.db import migrations, models
import django.utils.timezone
import shortuuid.main


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22, primary_key=True, serialize=False)),
                ('original_url', models.URLField(max_length=2048)),
                ('short_code', models.CharField(editable=False, max_length=8, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('redirect_count', models.IntegerField(default=0)),
            ],
        ),
    ]
