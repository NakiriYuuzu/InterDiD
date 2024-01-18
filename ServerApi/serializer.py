from rest_framework import serializers
from ServerCommon.models import *
from django.contrib.auth.models import User as Account


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'is_staff', 'is_superuser']


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'line_id', 'unique_code', 'create_at']


class ArtworkItemsSerializer(serializers.ModelSerializer):
    artwork_item_title = serializers.CharField(required=True)
    artwork_item_description = serializers.CharField(required=True)
    artwork_product_title = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ArtworkItems
        fields = ['artwork_item_id', 'artworks', 'artwork_item_image', 'artwork_item_title', 'artwork_item_description',
                  'artwork_product_title']

    def create(self, validated_data):
        # 使用 pop 方法的第二个参数提供默认值，这样如果 'artwork_product_title' 键不存在也不会引发 KeyError
        artwork_product_title = validated_data.pop('artwork_product_title', None)
        artwork_item = ArtworkItems.objects.create(**validated_data)

        # 如果提供了 artwork_product_title，则创建或获取 Artworks 实例
        if artwork_product_title:
            artwork, created = Artworks.objects.get_or_create(product_title=artwork_product_title)
            artwork_item.artworks = artwork  # 关联 Artworks 实例
            artwork_item.save()  # 保存 ArtworkItems 实例以更新 'artworks' 字段

        return artwork_item


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
