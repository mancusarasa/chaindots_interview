from typing import (
    List,
    Dict,
    Any,
    Optional,
)
from datetime import datetime

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

    def test_fetching_posts_filtering_by_author_returns_correct_set(self):
        user_one = self._create_user(1)
        user_two = self._create_user(2)
        token_one = self._login("user1", "pass1")
        token_two = self._login("user2", "pass2")
        posts_user_one = [self._create_post(i, token_one) for i in range(2)]
        posts_user_two = [self._create_post(i, token_two) for i in range(3)]
        fetched_posts_one = self._fetch_posts(token_one, user_one["id"])
        fetched_posts_two = self._fetch_posts(token_one, user_two["id"])
        self.assertEqual(len(fetched_posts_one["results"]), 2)
        for post in fetched_posts_one["results"]:
            self.assertEqual(post["author_id"], user_one["id"])
        self.assertEqual(len(fetched_posts_two["results"]), 3)
        for post in fetched_posts_two["results"]:
            self.assertEqual(post["author_id"], user_two["id"])

    def test_fetching_posts_without_author_retrieves_them_all(self):
        users_count = 10
        users = [self._create_user(i+1) for i in range(users_count)]
        tokens = [self._login(user["username"], f"pass{i+1}") for i, user in enumerate(users)]
        for user, token in zip(users, tokens):
            self._create_post(f"{user['username']} says: Hi!", token)
        posts = self._fetch_posts(tokens[0])
        self.assertEqual(posts["count"], users_count)
        for index, post in enumerate(posts["results"]):
            author_id = index + 1
            self.assertEqual(post["author_id"], author_id)
            self.assertEqual(post["content"], f"user{author_id} says: Hi!")
    
    def test_play_around_with_pagination_options(self):
        posts_count = 50
        user = self._create_user(1)
        token = self._login("user1", "pass1")
        for index in range(posts_count):
            self._create_post(f"Post {index}", token)
        # fetch using default pagination options (page = 1, page_size=20)
        posts = self._fetch_posts(token)["results"]
        self.assertEqual(len(posts), 20)
        posts_ids = set(post["id"] for post in posts)
        expected_posts_ids = set(i+1 for i in range(20))
        self.assertEqual(posts_ids, expected_posts_ids)
        # fetch using page_size=10, page=4
        posts = self._fetch_posts(
            token,
            author_id=None,
            page_size=10,
            page=4
        )["results"]
        posts_ids = set(post["id"] for post in posts)
        expected_posts_ids = set(i for i in range(31, 41))
        self.assertEqual(posts_ids, expected_posts_ids)

    def test_searching_in_date_ranges(self):
        posts_count = 50
        user = self._create_user(1)
        token = self._login("user1", "pass1")
        posts = [self._create_post(f"Post {index}", token) for index in range(posts_count)]
        middle_date = posts[25]["creation_date"]
        first_half = self._fetch_posts(
            token,
            author_id=None,
            page_size=50,
            page=1,
            from_date=None,
            to_date=middle_date
        )["results"]
        posts_ids = set(post["id"] for post in first_half)
        expected_post_ids = set(range(1, 27))
        self.assertEqual(posts_ids, expected_post_ids)
        second_half = self._fetch_posts(
            token,
            author_id=None,
            page_size=50,
            page=1,
            from_date=middle_date,
            to_date=None
        )["results"]
        posts_ids = set(post["id"] for post in second_half)
        expected_post_ids = set(range(26, 51))
        self.assertEqual(posts_ids, expected_post_ids)

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

    def _create_post(self, post_content: str, token: str) -> Dict[str, Any]:
        response = self.client.post(
            reverse('posts-list'),
            { "content": post_content },
            headers={"Authorization": f"Token {token}"},
            format="json"
        )
        return response.data

    def _get_user_details(self, user_id: int, token: str) -> Dict[str, Any]:
        return self.client.get(
            reverse(
                "user-details",
                kwargs={'pk': user_id}
            ),
            headers={"Authorization": f"Token {token}"}
        ).data

    def _fetch_posts(
        self,
        token: str,
        author_id: Optional[int] = None,
        page_size: int = 20,
        page: int = 1,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Dict]:
        data = {
            "page_size": page_size,
            "page": page,
        }
        if author_id is not None:
            data["author_id"] = author_id
        if from_date is not None:
            data["from_date"] = from_date
        if to_date is not None:
            data["to_date"] = to_date
        return self.client.get(
            reverse(
                'posts-list',
            ),
            data=data,
            headers={"Authorization": f"Token {token}"},
            format="json"
        ).data
