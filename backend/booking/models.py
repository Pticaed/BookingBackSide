import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Property(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    blockchain_id = models.IntegerField(
        blank=True,
        null=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    price_per_night = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    booked_dates = models.JSONField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "properties"
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["city"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        return self.title


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    blockchain_id = models.IntegerField(
        blank=True,
        null=True
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guest_bookings"
    )

    check_in = models.DateField()
    check_out = models.DateField()

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    blockchain_tx = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "bookings"
        indexes = [
            models.Index(fields=["property"]),
            models.Index(fields=["guest"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("check_out must be after check_in")

    def __str__(self):
        return f"Booking {self.id}"


class Review(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField()
    ipfs_cid = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    content_cache = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = "reviews"

    def clean(self):
        if not 1 <= self.rating <= 5:
            raise ValidationError("Rating must be between 1 and 5")

    def __str__(self):
        return f"Review {self.rating}"


class PriceHistory(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="price_history"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "price_history"
        indexes = [
            models.Index(fields=["property"]),
        ]

    def __str__(self):
        return f"{self.property} → {self.price}"