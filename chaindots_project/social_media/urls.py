from django.urls import path

from social_media.views import (
    UserListView,
    UserDetailsView,
    PostListView,
    PostDetailsView,
    FollowersView,
    CommentListView,
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
    path('posts/<int:post_id>/', PostDetailsView.as_view(), name='post-details'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comments-list'),
]
