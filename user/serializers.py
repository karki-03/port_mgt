
from rest_framework import serializers
from django.contrib.auth import get_user_model

custom_user = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = custom_user
        fields = ['id','email','password','is_staff','is_superuser','first_name','last_name',
        'is_active','last_login','date_joined','phone']
        read_only_fields = ('is_staff','is_superuser','last_login','date_joined','id','is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        return custom_user.objects.create_user(**validated_data)     

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(CustomUserSerializer, self).update(instance, validated_data)
            