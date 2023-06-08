from rest_framework import serializers
from .models import DirectMessage


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ("file",)
        