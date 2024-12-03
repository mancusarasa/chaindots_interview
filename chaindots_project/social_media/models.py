from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, blank=False)
