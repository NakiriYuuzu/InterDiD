from rest_framework import serializers
from ServerCommon.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'line_id', 'unique_code']


class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacons
        fields = ['beacon_id', 'beacon_name', 'beacon_UUID']
