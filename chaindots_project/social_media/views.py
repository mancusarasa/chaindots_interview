from django.shortcuts import render
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from django.core.paginator import (
    Paginator,
    EmptyPage
)
# these two imports might need to be moved
# to models.py
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms.models import model_to_dict

from social_media.models import (
    User,
    Post,
    Following,
    Comment,
)
from social_media.serializers import (
    UserSerializer,
    PostSerializer,
    FollowingSeralizer,
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
        author_id = request.GET.get('author_id', None)
        posts = Post.objects.filter(author_id=author_id) if author_id else Post.objects.all()
        page_size = request.GET.get('page_size', 20)
        page_number = request.GET.get('page_number', 1)
        paginator = Paginator(posts, page_size)
        try:
            page = paginator.page(page_number)
            serializer = PostSerializer(page.object_list, many=True)
            data = [post for post in serializer.data]
        except EmptyPage:
            data = []
        response = data
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist as e:
            return Response({'error': f'Post {post_id} does not exist'})
        return Response(model_to_dict(post), status.HTTP_200_OK)


class FollowersView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        follower_id = kwargs['follower_id']
        followed_id = kwargs['followed_id']
        try:
            user_one = User.objects.get(id=int(follower_id))
            user_two = User.objects.get(id=int(followed_id))
            Following.objects.create(
                follower_id=user_one,
                followed_id=user_two
            )
        except ObjectDoesNotExist as e:
            return Response(
                {'error': 'One of the users does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError:
            return Response(
                {'error': f'User {follower_id} already follows {followed_id}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({}, status=status.HTTP_200_OK)


class CommentListView(
    generics.GenericAPIView
):
    def get(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist as e:
            return Response(
                {'error': f'Post {post_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            model_to_dict(post),
            status=status.HTTP_200_OK
        )


    def post(self, request, *args, **kwargs):
        # FIXME: this is wrong, author_id must be 
        # obtained from the auth token
        author_id = request.data['author_id']
        post_id = kwargs['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist as e:
            return Response(
                {'error': f'Post {post_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            # FIXME: this might need to go once I'm
            # using auth tokens
            user = User.objects.get(id=author_id)
        except ObjectDoesNotExist as e:
            return Response(
                {'error': f'User {user_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        post_content = request.data['content']
        comment = Comment.objects.create(
            author_id=user,
            post_id=post,
            content=post_content
        )
        return Response(model_to_dict(comment), status=status.HTTP_200_OK)
