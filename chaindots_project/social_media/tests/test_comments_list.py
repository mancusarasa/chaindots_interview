from typing import (
    List,
    Dict,
    Any
)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestCommentsList(APITestCase):
    def test_comments_list_brings_all_comments(self):
        user_one = self._create_user(1)
        token_one = self._login("user1", "pass1")
        post = self._create_post("hello", token_one)
        user_two = self._create_user(2)
        user_three = self._create_user(3)
        user_four = self._create_user(4)
        user_five = self._create_user(5)
        self._create_comment(
            post["id"],
            self._login("user2", "pass2"),
            "comment 2"
        )
        self._create_comment(
            post["id"],
            self._login("user3", "pass3"),
            "comment 3"
        )
        self._create_comment(
            post["id"],
            self._login("user4", "pass4"),
            "comment 4"
        )
        self._create_comment(
            post["id"],
            self._login("user5", "pass5"),
            "comment 5"
        )
        comments = self._fetch_comments(post["id"], token_one)
        self.assertEqual(len(comments), 4)
        self.assertEqual(comments[0]["author_id"], user_two["id"])
        self.assertEqual(comments[1]["author_id"], user_three["id"])
        self.assertEqual(comments[2]["author_id"], user_four["id"])
        self.assertEqual(comments[3]["author_id"], user_five["id"])

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
            reverse("posts-list"),
            {
                "content": f"content of post {post_content}"
            },
            headers={"Authorization": f"Token {token}"},
            format="json"
        )
        return response.data

    def _fetch_comments(self, post_id: int, token: str) -> List[Dict]:
        return self.client.get(
            reverse(
                "comments-list",
                kwargs={"post_id": post_id}
            ),
            headers={"Authorization": f"Token {token}"},
            format="json"
        ).data

    def _create_comment(self, post_id: int, token: str, comment: str):
        return self.client.post(
            reverse(
                "comments-list",
                kwargs={'post_id': post_id}
            ),
            {"content": "comment"},
            headers={"Authorization": f"Token {token}"},
            format="json"
        )
