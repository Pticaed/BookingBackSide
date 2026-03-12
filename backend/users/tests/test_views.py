import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTestCase(TestCase):

    def setUp(self):
        self.wallet = '0x1234567890123456789014885678901234567890'
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
            wallet_address=self.wallet
        )
        self.list_url = reverse('user_list')
        self.detail_url = reverse('user_detail', kwargs={'wallet_address': self.wallet})

    def test_1_get_users_list(self):
        response = self.client.get(self.list_url)
        assert response.status_code == 200
        assert len(response.data['users']) >= 1

    def test_2_get_user_by_wallet(self):
        response = self.client.get(self.detail_url)
        assert response.status_code == 200
        assert response.data['username'] == 'testuser'
        assert response.data['wallet_address'] == self.wallet

    def test_3_create_user_success(self):
        data = {
            'username': 'newuser',
            'wallet_address': '0xABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABC',
            'email': 'new@test.com'
        }
        response = self.client.post(reverse('user_create'), data, content_type='application/json')
        assert response.status_code == 201
        assert User.objects.filter(username='newuser').exists()

    def test_4_create_user_duplicate_wallet(self):
        data = {
            'username': 'otheruser',
            'wallet_address': self.wallet,
            'email': 'blablabla@test.com'
        }
        response = self.client.post(reverse('user_create'), data, content_type='application/json')
        assert response.status_code == 400

    def test_5_update_user_profile(self):
        data = {'email': 'updated@test.com'}
        url = reverse('user_update', kwargs={'wallet_address': self.wallet})
        response = self.client.patch(url, data, content_type='application/json')
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.email == 'updated@test.com'

    def test_6_delete_user(self):
        url = reverse('user_delete', kwargs={'wallet_address': self.wallet})
        response = self.client.delete(url)
        assert response.status_code == 204
        assert User.objects.filter(wallet_address=self.wallet).count() == 0