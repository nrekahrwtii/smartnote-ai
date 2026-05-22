from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=200
    )

    lecturer = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    meeting = models.IntegerField(
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    summary = models.TextField(
        blank=True,
        null=True
    )

    file = models.FileField(
        upload_to='materials/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title