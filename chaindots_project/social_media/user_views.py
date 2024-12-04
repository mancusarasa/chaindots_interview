from rest_framework import (
    generics,
    permissions
)
from django.contrib.auth.models import User
from django.db.models import Count

from social_media.serializers import (
    UserSerializer,
    UserExtraInfoSerializer
)

class UserListView(
    generics.CreateAPIView,
    generics.ListAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetailsView(
    generics.RetrieveAPIView
):
    serializer_class = UserExtraInfoSerializer

    def get_queryset(self):
        return User.objects.annotate(
            total_posts=Count('post', distinct=True)
        ).annotate(
            total_comments=Count('comment', distinct=True)
        ).all()
