# Chaindots interview exercise

This is the interview exercise for Chaindots.

# Endpoints

1. GET /api/users/: Retrieve a list of all users. (X)
2. POST /api/users/: Create a new user. (X)
3. GET /api/users/{id}/: Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following.
4. POST /api/posts/: Create a new post. (X)
5. POST /api/users/{id}/follow/{id}: Set first id user as follower of second id user. (X)
6. GET /api/posts/: Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. The filters to implement are: author_id, from_date, to_date. None of the filters is compulsory. The pagination should be achieved with the following parameters: page_size (default = 20), page_number (default = 1) (X)
7. POST /api/posts/{id}/comments/: Add a new comment to a post. (X)
8. GET /api/posts/{id}/comments/: Retrieve all comments for a specific post. (X)
9. GET /api/posts/{id}/: Retrieve details of a specific post with its' last three comments included and the information of its creator.

# Commands:

1. Retrieve a list of all users:

`curl -H "Content-type: application/json" -X GET localhost:8000/api/users/`

2. Create a new user:

`curl -H "Content-type: application/json" -X POST -d '{"username": "user1", "email": "user1@hotmail.com", "password": "pass1"}' localhost:8000/api/users/`

2. Login with the new user:

`export TOKEN=$(curl -H "Content-type: application/json" -X POST -d '{"username": "user1", "password": "pass1"}' "localhost:8000/api/login/" | jq -r '.token')`

This token will be useful to validate all the requests below, through the `Authorization: Token` header.

3. Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following:

`curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET localhost:8000/api/users/1/`

4. Create a new post

`curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -d '{"author_id": 1, "content": "a post"}' -X POST localhost:8000/api/posts/`

5. Set first id user as follower of second id user

`curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/users/1/follow/1/`

6. Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. The filters to implement are: author_id, from_date, to_date. None of the filters is compulsory. The pagination should be achieved with the following parameters: page_size (default = 20), page_number (default = 1):

`curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET "localhost:8000/api/posts/?author_id=1&page_size=1&page=2"`

7. Add a new comment to a post:

`curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X POST -d '{"content": "a new post"}' localhost:8000/api/posts/1/comments/`

8. Retrieve all comments for a specific post:

`curl -H "Content-type: application/json" -H "Authorization: Token $TOKEN" -X GET localhost:8000/api/posts/1/comments/`
