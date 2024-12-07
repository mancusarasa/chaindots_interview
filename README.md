# Chaindots interview exercise

This is the interview exercise for Chaindots.

# Endpoints

1. GET /api/users/: Retrieve a list of all users. (X)
2. POST /api/users/: Create a new user. (X)
3. GET /api/users/{id}/: Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following. (X)
4. POST /api/posts/: Create a new post. (X)
5. POST /api/users/{id}/follow/{id}: Set first id user as follower of second id user. (X)
6. GET /api/posts/: Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. The filters to implement are: author_id, from_date, to_date. None of the filters is compulsory. The pagination should be achieved with the following parameters: page_size (default = 20), page_number (default = 1) (X)
7. POST /api/posts/{id}/comments/: Add a new comment to a post. (X)
8. GET /api/posts/{id}/comments/: Retrieve all comments for a specific post. (X)
9. GET /api/posts/{id}/: Retrieve details of a specific post with its' last three comments included and the information of its creator. (X)

# How to use the API

1. Retrieve a list of all users:

```shell
curl -H "Content-type: application/json" -X GET localhost:8000/api/users/
```

2. Create a new user:

```shell
curl -H "Content-type: application/json" -X POST -d '{"username": "user1", "email": "user1@hotmail.com", "password": "pass1"}' localhost:8000/api/users/
```

2. Login with the new user:

```shell
export TOKEN=$(curl -H "Content-type: application/json" -X POST -d '{"username": "user1", "password": "pass1"}' "localhost:8000/api/login/" | jq -r '.token')
```

This token will be useful to validate all the requests below, through the `Authorization: Token` header.

3. Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following:

```shell
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET localhost:8000/api/users/1/
```

4. Create a new post

```shell
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -d '{"content": "a post"}' -X POST localhost:8000/api/posts/
```

5. Set first id user as follower of second id user

```shell
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/1/follow/1/
```

6. Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. The filters to implement are: author_id, from_date, to_date. None of the filters is compulsory. The pagination should be achieved with the following parameters: page_size (default = 20), page_number (default = 1):

```shell
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET "localhost:8000/api/posts/?author_id=1&page_size=1&page=2"
```

7. Add a new comment to a post:

```shell
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST -d '{"content": "a new post"}' localhost:8000/api/posts/1/comments/
```

8. Retrieve all comments for a specific post:

```shell
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET localhost:8000/api/posts/1/comments/
```

# Usage example

```shell

# Create 9 users:
curl -H "Content-type: application/json" -X POST -d '{"username": "user1", "email": "user1@hotmail.com", "password": "pass1"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user2", "email": "user2@hotmail.com", "password": "pass2"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user3", "email": "user3@hotmail.com", "password": "pass3"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user4", "email": "user4@hotmail.com", "password": "pass4"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user5", "email": "user5@hotmail.com", "password": "pass5"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user6", "email": "user6@hotmail.com", "password": "pass6"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user7", "email": "user7@hotmail.com", "password": "pass7"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user8", "email": "user8@hotmail.com", "password": "pass8"}' localhost:8000/api/users/
curl -H "Content-type: application/json" -X POST -d '{"username": "user9", "email": "user9@hotmail.com", "password": "pass9"}' localhost:8000/api/users/

# Login with user1
export TOKEN=$(curl -H "Content-type: application/json" -X POST -d '{"username": "user1", "password": "pass1"}' "localhost:8000/api/login/" | jq -r '.token')

# Make user1 follow 3 users:
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/1/follow/2/
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/1/follow/3/
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/1/follow/4/

# Make user6 and user7 follow user1:
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/4/follow/1/
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/5/follow/1/

# Create two posts with user1:
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -d '{"content": "post 1"}' -X POST localhost:8000/api/posts/
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -d '{"content": "post 2"}' -X POST localhost:8000/api/posts/

# Check the amount of posts, followers/following of user1
curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET localhost:8000/api/users/1/
```

# Pending tests

I could have done some more tests that included more combinations of pagination settings, and also play around with disabling the `author_id` field. However, I feel I provided enought unit tests to assert that the presented API behaves like it was specified.
