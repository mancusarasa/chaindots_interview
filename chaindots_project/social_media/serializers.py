from rest_framework import serializers
from django.contrib.auth.models import User

from social_media.models import (
    Post,
    Following,
    Comment,
)


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

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

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserExtraInfoSerializer(UserSerializer):

    total_posts = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_followers = serializers.IntegerField()
    total_following = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "total_posts",
            "total_comments",
            "total_followers",
            "total_following",
        ]


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


class FollowingSerializer(serializers.ModelSerializer):
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author_id", "post_id", "content"]
        extra_kwargs = {
            "author_id": {
                "error_messages": {
                    "required": "author_id is required",
                },
            },
            "post_id": {
                "error_messages": {
                    "required": "Followed_id is required",
                },
            },
            "content": {
                "error_messages": {
                    "required": "content is required",
                },
            },
        }
