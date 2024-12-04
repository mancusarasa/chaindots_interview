from rest_framework import (
    permissions,
    generics,
    mixins
)
from django.core.paginator import (
    Paginator,
    EmptyPage
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from social_media.models import (
    Post,
)
from social_media.serializers import (
    PostSerializer
)


# FIXME: this is lacking the last three comments included and the information of its creator.
class PostDetailsView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)


class PostsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class PostListView(
    generics.ListAPIView,
    mixins.CreateModelMixin
):
    serializer_class = PostSerializer
    pagination_class = PostsPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get('author_id')
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        from_date = self.request.query_params.get('from_date')
        if from_date is not None:
            queryset = queryset.filter(creation_date__gt=from_date)
        to_date = self.request.query_params.get('to_date')
        if to_date is not None:
            queryset = queryset.filter(creation_date__lt=to_date)
        return queryset

    def post(self, request, *args, **kwargs):
        # FIXME: maybe find a way to do this automagically
        request.data['author_id'] = request.user.id
        return self.create(request, *args, **kwargs)
