# Chaindots interview exercise

This is the interview exercise for Chaindots.

# Endpoints

Done:
- GET /api/users/: Retrieve a list of all users.
- POST /api/users/: Create a new user.
- GET /api/users/{id}/: Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following.
- POST /api/posts/: Create a new post.

In progress:

Not done:
- POST /api/users/{id}/follow/{id}: Set first id user as follower of second id user.
- GET /api/posts/: Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. The filters to implement are: author_id, from_date, to_date. None of the filters is compulsory. The pagination should be achieved with the following parameters: page_size (default = 20), page_number (default = 1)
- GET /api/posts/{id}/: Retrieve details of a specific post with its' last three comments included and the information of it&#39;s creator.
- GET /api/posts/{id}/comments/: Retrieve all comments for a specific post.
- POST /api/posts/{id}/comments/: Add a new comment to a post.

# Next steps:

- Incorporate the usage of django rest auth tokens.
- Implement authentication on relevant endpoints using tokens.


# Commands:

- Fetch all users:

`curl -H "Content-type: application/json" -X GET localhost:8000/api/users/`

- Fetch all posts:

`curl -H "Content-type: application/json" -X GET localhost:8000/api/posts/`

- Create a post (in this context the user_id comes in the body. this is wrong, user_id must be obtained from the token when we have authentication)

`curl -H "Content-type: application/json" -d '{"author": 1, "content": "a post"}' -X POST localhost:8000/api/posts/`
