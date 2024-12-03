from rest_framework import serializers

from social_media.models import (
    User,
    Post,
    Following,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
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
        fields = ["author_id", "content", "creation_date"]
        extra_kwargs = {
            "author_id": {
                "error_messages": {
                    "required": "Author_id is required",
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


class FollowingSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ["follower_id", "followed_id"]
        extra_kwargs = {
            "follower_id": {
                "error_messages": {
                    "required": "Follower_id is required",
                },
            },
            "followed_id": {
                "error_messages": {
                    "required": "Followed_id is required",
                },
            },
        }
