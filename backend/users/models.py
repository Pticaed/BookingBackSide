from django.db import models
import uuid
from django.db import models


# Create your models here.


class User(models.Model):
    wallet_address = models.CharField(
        max_length=255,
        primary_key=True
    )

    username = models.CharField(max_length=255)

    email = models.EmailField(
        unique=True
    )

    avatar_url = models.URLField(
        blank=True,
        null=True
    )

    avg_rating = models.FloatField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return self.username