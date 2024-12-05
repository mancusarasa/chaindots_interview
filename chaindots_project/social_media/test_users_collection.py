from typing import (
    List,
    Dict,
    Any
)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserCollection(APITestCase):
    def test_user_is_created_with_correct_fields(self):
        initial_collection = self.client.get(reverse("users-list")).data
        self.assertEqual(initial_collection, [])
        new_user = self._assert_user_is_created_correctly({
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "pass1",
        }, ignore_fields=["password"])
        collection = self.client.get(reverse("users-list")).data
        self.assertEqual(collection, [new_user])

    def test_login_with_incorrect_password_returns_error(self):
        new_user = self._assert_user_is_created_correctly({
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "pass1",
        }, ignore_fields=["password"])
        response = self.client.post(
            reverse("login"),
            {
                "username": "user1",
                "password": "wrong_password",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_correct_password_returns_ok(self):
        new_user = self._assert_user_is_created_correctly(
            {
                "username": "user1",
                "email": "user1@hotmail.com",
                "password": "pass1",
            },
            ignore_fields=["password"]
        )
        response = self._login("user1", "pass1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_details_returns_totals_in_zero(self):
        new_user = self._assert_user_is_created_correctly({
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "pass1",
        }, ignore_fields=["password"])
        response = self._login("user1", "pass1")
        token = response.data["token"]
        user_details = self.client.get(
            reverse(
                "user-details",
                kwargs={'pk': new_user["id"]}
            ),
            headers={"Authorization": f"Token {token}"}
        ).data
        self.assertEqual(user_details["username"], new_user["username"])
        self.assertEqual(user_details["email"], new_user["email"])
        self.assertEqual(user_details["total_posts"], 0)
        self.assertEqual(user_details["total_comments"], 0)
        self.assertEqual(user_details["total_followers"], 0)
        self.assertEqual(user_details["total_following"], 0)

    def _assert_user_is_created_correctly(
        self,
        user_data: Dict[str, Any],
        ignore_fields: List[str]
    ):
        response = self.client.post(reverse("users-list"), user_data)
        user = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for field, value in user_data.items():
            if field not in ignore_fields:
                self.assertEqual(user[field], value)
        return user

    def _login(self, username: str, password: str):
        return self.client.post(
            reverse("login"),
            {
                "username": username,
                "password": password,
            }
        )
