from rest_framework import serializers

from social_media.models import (
    User,
    Post,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            "username": {
                "error_messages": {
                    "required": "Username is required",
                },
            },
            "email": {
                "error_messages": {
                    "required": "Email is required",
                },
            },
            "password": {
                "error_messages": {
                    "required": "Password is required",
                },
            },
        }


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'content', 'creation_date']
        extra_kwargs = {
            "author": {
                "error_messages": {
                    "required": "Author is required",
                },
            },
            "content": {
                "error_messages": {
                    "required": "Content is required",
                },
            },
            "creation_date": {
                "error_messages": {
                    "required": "Creation date is required",
                },
            },
        }
