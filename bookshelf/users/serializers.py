from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username","email")
        
class ProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(many=False)
    
    class Meta:
        model = Profile
        exclude = ("id", )
        
    def update(self, instance, validated_data):
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.info = validated_data.get('info', instance.info)
        
        return instance