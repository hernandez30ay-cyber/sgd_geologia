from rest_framework import serializers
from .models import Document, DocumentMetadata

class DocumentMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentMetadata
        fields = ["id", "clave", "valor"]

class DocumentSerializer(serializers.ModelSerializer):
    metadatos = DocumentMetadataSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = "__all__"
