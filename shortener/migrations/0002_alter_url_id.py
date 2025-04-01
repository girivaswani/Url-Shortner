# Generated by Django 4.2.20 on 2025-03-14 21:58

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22, primary_key=True, serialize=False),
        ),
    ]
