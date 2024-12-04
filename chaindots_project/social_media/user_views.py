from rest_framework import (
    generics,
    permissions
)
from django.contrib.auth.models import User

from social_media.serializers import (
    UserSerializer
)

class UserListView(
    generics.ListAPIView,
    generics.CreateAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
