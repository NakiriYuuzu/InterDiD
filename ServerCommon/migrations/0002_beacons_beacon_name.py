# Generated by Django 4.2.6 on 2023-10-19 14:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ServerCommon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beacons',
            name='beacon_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]