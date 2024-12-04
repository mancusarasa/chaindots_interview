from django.db import models

from django.contrib.auth.models import User


class Following(models.Model):
    follower_id = models.ForeignKey(
        User,
        related_name='asd',
        on_delete=models.CASCADE
    )
    followed_id = models.ForeignKey(
        User,
        related_name='qwe',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.follower_id} -> {self.followed_id}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'follower_id',
                    'followed_id'
                ],
                name='unique_follower_followed'
            )
        ]


class Post(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creation_date']


class Comment(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, blank=False)
