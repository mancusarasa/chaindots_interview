from rest_framework import (
    generics,
    mixins,
    status
)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from social_media.models import (
    Post,
    Comment
)
from social_media.serializers import CommentSerializer
from django.forms.models import model_to_dict


class CommentListView(
    generics.ListAPIView,
    mixins.CreateModelMixin,
):
    serializer_class = CommentSerializer
    lookup_field = "post_id"

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        queryset = Comment.objects.all().filter(post_id=post_id)
        return queryset

    def post(self, request, *args, **kwargs):
        request.data["author_id"] = request.user.id
        request.data["post_id"] = kwargs["post_id"]
        return self.create(request, *args, **kwargs)
