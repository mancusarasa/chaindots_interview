from django.urls import path

from rest_framework.authtoken import views

from social_media.user_views import (
    UserListView,
    UserDetailsView
)
from social_media.post_views import (
    PostDetailsView,
    PostListView
)
from social_media.followers_views import (
    FollowersView
)
from social_media.comment_views import (
    CommentListView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetailsView.as_view(), name='user-details'),
    path(
        'users/<int:follower_id>/follow/<int:followed_id>/',
        FollowersView.as_view(),
        name='follow-user'
    ),
    path('posts/', PostListView.as_view(), name='posts-list'),
    path('posts/<int:pk>/', PostDetailsView.as_view(), name='post-details'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comments-list'),
    path('login/', views.obtain_auth_token),
]
