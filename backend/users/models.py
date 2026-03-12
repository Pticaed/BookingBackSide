from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wallet_address = models.CharField(
        max_length=255, 
        unique=True, 
        null=True, 
        blank=True
    )
    avatar_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True
    )
    avg_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["wallet_address"]),
        ]

    def __str__(self):
        return f"{self.username} ({self.wallet_address or 'No Wallet'})"