import pytest
import json
from django.db import transaction
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from booking.models import Property, Booking

User = get_user_model()

class BlockchainEventsTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create(
            username='owner',
            email='owner@test.com',
            wallet_address='0x1234567890123456789012345678901234567890'
        )

        self.guest = User.objects.create(
            username='guest',
            email='guest@test.com',
            wallet_address='0x0987654321098765432109876543210987654321'
        )

        self.property = Property.objects.create(
            owner=self.owner,
            title='Test Property',
            city='Kyiv',
            country='Ukraine',
            price_per_night=100.00,
            blockchain_id=1
        )

        self.booking = Booking.objects.create(
            property=self.property,
            guest=self.guest,
            check_in='2026-04-01',
            check_out='2026-04-05',
            total_amount=400.00,
            status='pending'
        )

    def test_1_booking_initial_state(self):
        assert self.booking.status == 'pending'
        assert self.booking.blockchain_id is None
        assert self.booking.blockchain_tx is None

    def test_2_find_booking_by_wallet(self):
        booking = Booking.objects.filter(
            property=self.property,
            guest=self.guest,
            status='pending'
        ).first()
        
        assert booking is not None
        assert booking.id == self.booking.id

    def test_6_process_new_booking_event(self):
        event = {
            'args': {
                'id': 101,
                'property_id': 1,
                'guest': self.guest.wallet_address,
                'amount': 400
            },
            'transactionHash': b'\xaa' * 32
        }
        
        args = event['args']
        tx_hash = event['transactionHash'].hex()
        
        property_obj = Property.objects.filter(blockchain_id=args['property_id']).first()
        assert property_obj is not None
        
        booking = Booking.objects.filter(
            property=property_obj,
            guest__wallet_address__iexact=args['guest'],
            status='pending'
        ).first()
        
        assert booking is not None
        
        with transaction.atomic():
            booking.blockchain_id = args['id']
            booking.blockchain_tx = tx_hash
            booking.status = 'confirmed'
            booking.save()
        
        booking.refresh_from_db()
        assert booking.status == 'confirmed'
        assert booking.blockchain_id == 101
        assert booking.blockchain_tx == tx_hash

    def test_8_transaction_rollback_on_error(self):
        original_status = self.booking.status
        
        try:
            with transaction.atomic():
                self.booking.status = 'confirmed'
                self.booking.save()
                raise ValueError("Simulated database failure")
        except ValueError:
            pass
        
        self.booking.refresh_from_db()
        assert self.booking.status == original_status

    def test_10_missing_property_doesnt_crash(self):
        exists = Property.objects.filter(blockchain_id=999).exists()
        assert exists is False