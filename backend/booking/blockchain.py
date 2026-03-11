import json
from web3 import Web3
from django.conf import settings
from django.db import transaction
from .models import Property, Booking

class BlockchainEvents:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
        self.contract_address = settings.CONTRACT_ADDRESS
        
        with open(settings.BLOCKCHAIN_ABI_PATH, 'r') as file:
            self.abi = json.load(file)
        
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

    def sync_events(self, from_block='latest', to_block='latest'):
        self._sync_new_bookings(from_block, to_block)
        self._sync_booking_statuses(from_block, to_block)

    def _sync_new_bookings(self, from_block, to_block):
        event_filter = self.contract.events.NewBooking.create_filter(
            fromBlock=from_block, 
            toBlock=to_block
        )
        events = event_filter.get_all_entries()

        for event in events:
            try:
                args = event['args']
                b_id = args['id']
                prop_id = args['property_id']
                guest_wallet = args['guest']
                tx_hash = event['transactionHash'].hex()

                if Booking.objects.filter(blockchain_id=b_id).exists():
                    continue

                try:
                    property_obj = Property.objects.get(blockchain_id=prop_id)
                except Property.DoesNotExist:
                    continue

                booking = Booking.objects.filter(
                    property=property_obj,
                    guest__wallet_address__iexact=guest_wallet,
                    status='pending'
                ).order_by('-created_at').first()

                if booking:
                    with transaction.atomic():
                        booking.blockchain_id = b_id
                        booking.blockchain_tx = tx_hash
                        booking.status = 'confirmed'
                        booking.save()

            except Exception as e:
                continue

    def _sync_booking_statuses(self, from_block, to_block):
        event_filter = self.contract.events.BookingStatusChanged.create_filter(
            fromBlock=from_block, 
            toBlock=to_block
        )
        events = event_filter.get_all_entries()

        for event in events:
            try:
                args = event['args']
                b_id = args['id']
                new_status = args['status']

                try:
                    booking = Booking.objects.get(blockchain_id=b_id)
                except Booking.DoesNotExist:
                    continue

                valid_statuses = dict(Booking.STATUS_CHOICES).keys()
                status_str = str(new_status).lower().strip()
                
                if status_str in valid_statuses:
                    with transaction.atomic():
                        booking.status = status_str
                        booking.save()

            except Exception as e:
                continue