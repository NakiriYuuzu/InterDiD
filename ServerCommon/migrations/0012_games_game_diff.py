# Generated by Django 4.2.6 on 2024-01-19 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServerCommon', '0011_alter_artworkitems_artwork_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='game_diff',
            field=models.IntegerField(null=True),
        ),
    ]
