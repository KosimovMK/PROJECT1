import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(unique=True, editable=False,
                          default=uuid.uuid4, primary_key=True)
