from django.urls import path

from social_media.views import (
    UserListView,
    UserDetailsView,
    PostListView,
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>', UserDetailsView.as_view(), name='user-details'),
    path('posts/', PostListView.as_view(), name='posts-list'),
]
