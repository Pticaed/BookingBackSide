import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from booking.models import Property, Booking, Review

User = get_user_model()

class BookingSystemTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create(
            username='owner_user',
            wallet_address='0xOWNER12345678901234567890123456789012345'
        )
        self.guest = User.objects.create(
            username='guest_user',
            wallet_address='0xGUEST12345678901234567890123456789012345'
        )
        self.property = Property.objects.create(
            owner=self.owner,
            title='Luxury Villa',
            city='Nicca',
            country='Georgia',
            price_per_night=100.00
        )
        self.booking = Booking.objects.create(
            property=self.property,
            guest=self.guest,
            check_in='2026-06-01',
            check_out='2026-06-05',
            total_amount=400.00,
            status='confirmed'
        )

    def test_1_property_list_and_filter(self):
        url = reverse('property_list')
        response = self.client.get(url, {'city': 'Nicca'})
        assert response.status_code == 200
        assert response.data[0]['title'] == 'Luxury Villa'

    def test_2_check_availability_occupied(self):
        url = reverse('property_availability', kwargs={'pk': self.property.id})
        data = {'check_in': '2026-06-03', 'check_out': '2026-06-07'}
        response = self.client.get(url, data)
        assert response.data['is_available'] is False

    def test_3_create_review(self):
        url = reverse('review_create')
        data = {
            'booking': self.booking.id,
            'rating': 5.0,
            'content_cache': 'nice place'
        }
        response = self.client.post(url, data, content_type='application/json')
        assert response.status_code == 201
        assert Review.objects.filter(booking=self.booking).exists()

    def test_4_get_price_history(self):
        url = reverse('property_price_history', kwargs={'pk': self.property.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_5_booking_delete(self):
        url = reverse('booking_delete', kwargs={'pk': self.booking.id})
        response = self.client.delete(url)
        assert response.status_code == 204
        assert Booking.objects.filter(pk=self.booking.id).count() == 0