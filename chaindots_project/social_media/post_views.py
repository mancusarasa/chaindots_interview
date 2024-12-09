from rest_framework import (
    permissions,
    generics,
    mixins,
    status
)
from django.core.paginator import (
    Paginator,
    EmptyPage
)
from django.forms.models import model_to_dict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from social_media.models import (
    Post,
)
from social_media.serializers import (
    PostSerializer,
    UserSerializer
)


class PostDetailsView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # FIXME: maybe improve this implementation?
        try:
            post_id = kwargs["post_id"]
            post = Post.objects.prefetch_related("post_comments").get(id=post_id)
            comments = post.post_comments.all().order_by("-creation_date")[0:3]
        except Post.DoesNotExist:
            return Response(
                {"error": "post f{post_id} not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        user_serializer = UserSerializer(post.author_id)
        post = model_to_dict(post)
        comments = [model_to_dict(comment) for comment in comments]
        return Response(
            data={
                **post,
                "latest_comments": comments,
                "author_info": user_serializer.data
            },
            status=status.HTTP_200_OK
        )


class PostsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"


class PostListView(
    generics.ListAPIView,
    mixins.CreateModelMixin
):
    serializer_class = PostSerializer
    pagination_class = PostsPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get("author_id")
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        from_date = self.request.query_params.get("from_date")
        if from_date is not None:
            queryset = queryset.filter(creation_date__gte=from_date)
        to_date = self.request.query_params.get("to_date")
        if to_date is not None:
            queryset = queryset.filter(creation_date__lte=to_date)
        return queryset

    def post(self, request, *args, **kwargs):
        request.data["author_id"] = request.user.id
        return self.create(request, *args, **kwargs)
