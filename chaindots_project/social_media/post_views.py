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
        # FIXME: maybe find a way to do this automagically
        request.data['author_id'] = request.user.id
        return self.create(request, *args, **kwargs)
