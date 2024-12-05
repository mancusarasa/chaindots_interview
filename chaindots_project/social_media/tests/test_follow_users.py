from typing import (
    List,
    Dict,
    Any
)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestFollowUsers(APITestCase):
    def test_following_users_summarizes_total_followers(self):
        users_count = 10
        users = [self._create_user(i+1) for i in range(users_count)]
        # login as user 1
        token = self._login("user1", "pass1")
        # make user 1 follow 3 users
        self._add_follower(1, 2, token)
        self._add_follower(1, 3, token)
        self._add_follower(1, 4, token)
        # make users 6 and 7 follow user1
        self._add_follower(6, 1, token)
        self._add_follower(7, 1, token)
        user_one_details = self._get_user_details(1, token)
        self.assertEqual(
            user_one_details["total_followers"], 2
        )
        self.assertEqual(
            user_one_details["total_following"], 3
        )


    def _create_user(self, user_id: int) -> Dict[str, Any]:
        return self.client.post(
            reverse("users-list"),
            {
                "username": f"user{user_id}",
                "password": f"pass{user_id}",
                "email": f"user{user_id}@hotmail.com",
            }
        ).data

    def _login(self, username: str, password: str) -> str:
        return self.client.post(
            reverse("login"),
            {
                "username": username,
                "password": password,
            }
        ).data["token"]

    def _add_follower(self, follower_id: int, followed_id: int, token: str):
        self.client.post(
            reverse(
                "follow-user",
                kwargs={"follower_id": follower_id, "followed_id": followed_id}
            ),
            headers={"Authorization": f"Token {token}"}
        )

    def _get_user_details(self, user_id: int, token: str) -> Dict[str, Any]:
        return self.client.get(
            reverse(
                "user-details",
                kwargs={'pk': user_id}
            ),
            headers={"Authorization": f"Token {token}"}
        ).data
