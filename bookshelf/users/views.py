import djoser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import render
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import signals
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from . import swagger
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer


class UserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    @swagger_auto_schema(
        manual_parameters=[swagger.username_param],
        responses={
            '200': 'OK',
            '404': 'Not Found',
            '400': 'Bad request',
        },
        operation_id="get_user_by_username",
        operation_description="""
            User authenticated required.
            Поиск пользователя по username.
        """
    )
    def get(self, request):
        username = request.GET.get("username", None)
        if not username:
            return Response(status=400, data="A username were not provided")
        
        users = User.objects.filter(username=username)
        
        if not users:
            return Response(status=404, data="A user with this username doesn't exist")
        
        user = None
        
        try:
            token = Token.objects.get(key=request.auth)
            user = User.objects.filter(username=username).exclude(id=token.user_id)
        except:
            user = User.objects.filter(username=username).exclude(id=request.user.id)
        
        if not user:
            return Response(status=404, data="You trying to find a user who have your nickname")

        profile = Profile.objects.get(user=user.get(username=username))
        serializer = ProfileSerializer(instance=profile)

        return Response(serializer.data, status=200)

class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)


class CustomRegistrationView(djoser.views.UserViewSet):

    def perform_create(self, serializer):
        user = serializer.save()
        Profile.objects.create(user=user, info={})
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)
            

class ProfileViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    @swagger_auto_schema(
        responses={
            '200': 'OK',
            '403': 'Forbidden',
        },
        operation_description="""
            User authenticated required.
            Возвращает данные профиля
        """
    )
    def get(self, request, *args, **kwargs):
        data = request.data
        profile = Profile.objects.get(user=request.user)
    
        serializer = ProfileSerializer(profile)
        
        return Response(status=200, data=serializer.data)
    
    @swagger_auto_schema(
        request_body=swagger.put_profile,
        responses={
            '200': 'OK',
            '204': 'NO CONTENT'
        },
        operation_description="""
            User authenticated required.
            Заменяет представленеие Profile. В случае, если какие-то поля не указаны, значения будут: null или ""
        """
    )
    def put(self, request, *args, **kwargs):
        data = request.data
        profile = Profile.objects.get(user=request.user)
        
        profile.first_name = data.get("first_name", "")
        profile.last_name = data.get("last_name", "")
        profile.birth_date = data.get("birth_date", None)
        profile.info = data.get("info", None)
        
        try: 
            profile.save()
        except ValidationError as e:
            return Response(status=400, data=e)
        
        serializer = ProfileSerializer(profile)
        
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=swagger.patch_profile,
        responses={
            '204': 'NO CONTENT'
        },
        operation_description="""
            User authenticated required.
            Частично обновляет Profile.
            
        """
    )
    def patch(self, request, *args, **kwargs):
        data = request.data
        profile = Profile.objects.get(user=request.user)
        
        serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        
        serializer.save()
        return Response(status=204)
            
        