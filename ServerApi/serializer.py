from rest_framework import serializers
from ServerCommon.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'line_id', 'unique_code', 'create_at']


class ArtworkItemsSerializer(serializers.ModelSerializer):
    artwork_item_title = serializers.CharField(required=True)
    artwork_item_description = serializers.CharField(required=True)

    class Meta:
        model = ArtworkItems
        fields = ['artwork_item_id', 'artworks', 'artwork_item_image', 'artwork_item_title', 'artwork_item_description']


class ArtworksSerializer(serializers.ModelSerializer):
    artwork_items = ArtworkItemsSerializer(read_only=True, many=True)

    class Meta:
        model = Artworks
        fields = ['artwork_id', 'product_title', 'artwork_items']


class BeaconsSerializer(serializers.ModelSerializer):
    artworks = ArtworksSerializer(read_only=True)

    class Meta:
        model = Beacons
        fields = ['beacon_id', 'beacon_name', 'beacon_uuid', 'artworks']


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['game_id', 'game_name']


class UserGamesSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    game = GamesSerializer(read_only=True)

    class Meta:
        model = UserGames
        fields = ['user_game_id', 'user', 'game', 'passed', 'play_date']
