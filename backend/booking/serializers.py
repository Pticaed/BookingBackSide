from rest_framework import serializers
from .models import Property, Booking, Review, PriceHistory

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'blockchain_id', 'owner', 'title', 
            'description', 'city', 'country', 
            'price_per_night', 'booked_dates', 'is_active'
        ]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'blockchain_id', 'property', 'guest', 
            'check_in', 'check_out', 'total_amount', 
            'blockchain_tx', 'status', 'created_at'
        ]
        read_only_fields = ['blockchain_tx', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'booking', 'rating', 'ipfs_cid', 'content_cache'
        ]

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = [
            'id', 'property', 'price', 'changed_at'
        ]