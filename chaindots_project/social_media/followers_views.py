from rest_framework import (
    generics,
    permissions,
    mixins,
)

from social_media.models import Following
from social_media.serializers import FollowingSerializer


class FollowersView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
):
    queryset = Following.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = FollowingSerializer

    def post(self, request, *args, **kwargs):
        follower_id = kwargs['follower_id']
        followed_id = kwargs['followed_id']
        # FIXME: maybe find a way to do this automagically
        request.data['follower_id'] = follower_id
        request.data['followed_id'] = followed_id
        return self.create(request, *args, **kwargs)
