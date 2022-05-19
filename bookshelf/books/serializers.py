
from rest_framework import serializers

from .models import Book
from users.serializers import ProfileSerializer


class BookSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(many=True)
    
    class Meta:
        model = Book
        fields = '__all__'
        

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('users',)