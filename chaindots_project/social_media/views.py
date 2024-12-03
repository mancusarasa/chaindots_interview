from django.shortcuts import render
from rest_framework import mixins, generics, status
from rest_framework.response import Response

from social_media.models import (
    User,
    Post,
)
from social_media.serializers import (
    UserSerializer,
    PostSerializer,
)


class UserListView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        response = [user for user in serializer.data]
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailsView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PostListView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        response = [post for post in serializer.data]
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, **kwargs)
