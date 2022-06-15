from rest_framework import serializers

from gdrive.models import GDFile


class GDFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = GDFile
        fields = '__all__'
