from rest_framework import serializers
from djoser.serializers import UserSerializer as DjUserSerializer

class UserSerializer(DjUserSerializer):
    class Meta(DjUserSerializer.Meta):
        pass



class APIKeySerializer(serializers.Serializer):

    client_id = serializers.CharField(read_only=True)
    appkey = serializers.CharField(read_only=True)


class UserCreateSerializer(serializers.Serializer):
    extra_data = serializers.JSONField()

    def create(self, validated_data):
        access_token = validated_data['extra_data']['access_token']

        pass






