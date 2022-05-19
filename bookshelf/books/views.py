from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import status

from users.models import Profile
from .models import Book
from .serializers import BookSerializer, BookCreateSerializer

# Create your views here.

class BookListAPIView(APIView):
    
    def get(self, request):
        data = Book.objects.all()
        serializer = BookSerializer(data, many=True)
        return Response(serializer.data)

class BookCreateAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookDetailAPIView(APIView):
    
    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, id, format=None):
        book = self.get_object(id)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class BookUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookUserListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404
        
    def get_profile(self, id):
        try:
            return Profile.objects.get(pk=id)
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request):
        data = Book.objects.all()
        serializer = BookSerializer(data, many=True)
        return Response(serializer.data)

class BookUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404
        
    def get_profile(self, id):
        try:
            return Profile.objects.get(pk=id)
        except Profile.DoesNotExist:
            raise Http404
    
    def post(self, request, id):
        token = Token.objects.get(key=request.auth)
        profile = self.get_profile(token.user_id)
        book = self.get_object(id)
        
        profile.books.add(book)

        return Response({
            "detail": f"Book with id: {id} were successfully added"
        })
    
    def delete(self, request, id):
        token = Token.objects.get(key=request.auth)
        profile = self.get_profile(token.user_id)
        book = self.get_object(id)
        
        profile.books.remove({
            "detail": f"Book with id: {id} were successfully deleted"
        })

        return Response(f"Book with id: {id} were successfully deleted")