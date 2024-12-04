from rest_framework import (
    generics,
    mixins,
    permissions,
    status
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from social_media.models import (
    Post,
    Comment
)
from social_media.serializers import CommentSerializer
from django.forms.models import model_to_dict


class CommentListView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Comment.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        # FIXME: maybe find a way to do this automagically
        request.data['post_id'] = kwargs['post_id']
        return self.retrieve(request, *args, **kwargs)
        # post_id = kwargs['post_id']
        # try:
        #     post = Post.objects.get(id=post_id)
        # except ObjectDoesNotExist as e:
        #     return Response(
        #         {'error': f'Post {post_id} does not exist'},
        #         status=status.HTTP_404_NOT_FOUND
        #     )

        # return Response(
        #     model_to_dict(post),
        #     status=status.HTTP_200_OK
        # )

    def post(self, request, *args, **kwargs):
        author_id = request.user.id
        post_id = kwargs['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist as e:
            return Response(
                {'error': f'Post {post_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
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
