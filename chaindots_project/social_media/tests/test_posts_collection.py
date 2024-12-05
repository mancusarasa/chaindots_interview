from typing import (
    List,
    Dict,
    Any
)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestPostsCollection(APITestCase):
    def test_creating_posts_increases_total_posts(self):
        new_user = self._create_user(1)
        token = self._login("user1", "pass1")
        posts_count = 2
        posts = [self._create_post(i, token) for i in range(posts_count)]
        user_details = self._get_user_details(new_user["id"], token)
        self.assertEqual(user_details["total_posts"], 2)

    def _login(self, username: str, password: str):
        return self.client.post(
            reverse("login"),
            {
                "username": username,
                "password": password,
            }
        ).data["token"]

    def _create_user(self, user_id: int) -> Dict[str, Any]:
        return self.client.post(
            reverse("users-list"),
            {
                "username": f"user{user_id}",
                "password": f"pass{user_id}",
                "email": f"user{user_id}@hotmail.com",
            }
        ).data

    def _create_post(self, post_content: int, token: str) -> Dict[str, Any]:
        response = self.client.post(
            reverse('posts-list'),
            {
                "content": f"content of post {post_content}"
            },
            headers={"Authorization": f"Token {token}"},
            format="json"
        )
        return response.data

    def _get_user_details(self, user_id: int, token) -> Dict[str, Any]:
        return self.client.get(
            reverse(
                "user-details",
                kwargs={'pk': user_id}
            ),
            headers={"Authorization": f"Token {token}"}
        ).data
