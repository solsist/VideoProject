# coding:utf-8

from django.db import models
from .video import Videos
from .auth import ClientUser


class CommentView(models.Model):
    content = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    video = models.ForeignKey(
        Videos,
        related_name='comment',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    user = models.ForeignKey(
        ClientUser,
        related_name='comment',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return self.content

    def data(self):
        return {
            'id': self.id,
            'content': self.content,
            'video_id': self.video.id,
            'user_id': self.user.id,
            'username': self.user.username
        }
