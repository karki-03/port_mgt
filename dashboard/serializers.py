from rest_framework import serializers
from .models import  *
"Serializer for model - File"

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = '__all__'

class DumpSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Dump
        fields = '__all__'
        read_only_fields = ('created_on','last_modified','fingerprint','owner','fields','tables')

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ('created_on','last_modified','fingerprint','fields',)

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        read_only_fields = ('created_on','last_modified','fingerprint','field_type')