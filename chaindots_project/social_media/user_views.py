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
    # 3. GET /api/users/{id}/: Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following.
    serializer_class = UserExtraInfoSerializer

    def get_queryset(self):
        # FIXME: might not need to make it dynamic
        return User.objects.annotate(
            total_posts=Count('post', distinct=True)
        ).annotate(
            total_comments=Count('comment', distinct=True)
        ).all()
