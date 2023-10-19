from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    line_id = models.CharField(max_length=255, unique=True)
    unique_code = models.CharField(max_length=10, null=True, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'yuuzu_users'


class Artworks(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    product_title = models.CharField(max_length=255)

    def __str__(self):
        return self.artwork_id

    class Meta:
        db_table = 'yuuzu_artworks'


class ArtworkItems(models.Model):
    artwork_item_id = models.AutoField(primary_key=True)
    artworks = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    artwork_item_image = models.CharField(max_length=255)
    artwork_item_title = models.CharField(max_length=255)
    artwork_item_description = models.TextField()

    def __str__(self):
        return self.artwork_item_title

    class Meta:
        db_table = 'yuuzu_artwork_items'


class Beacons(models.Model):
    beacon_id = models.AutoField(primary_key=True)
    beacon_name = models.CharField(max_length=255)
    beacon_uuid = models.CharField(max_length=100, unique=True)
    artworks = models.ForeignKey(Artworks, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.beacon_uuid

    class Meta:
        db_table = 'yuuzu_beacons'


class Games(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=255)

    def __str__(self):
        return self.game_name

    class Meta:
        db_table = 'yuuzu_games'


class UserGames(models.Model):
    user_game_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    play_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_game_id

    class Meta:
        db_table = 'yuuzu_user_games'
