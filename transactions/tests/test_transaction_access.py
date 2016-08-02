from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

import datetime
from decimal import Decimal
import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from transactions.models import Transaction
from transactions.views import TransactionDetail


class TransactionAccessTests(TestCase):
    def setUp(self):
        factory = APIRequestFactory()
        self.user = User.objects.create(username='user')
        self.user2 = User.objects.create(username='user2')
        self.tx = Transaction.objects.create(user=self.user,
                                             date=datetime.date(2016, 8, 2),
                                             payee='Payee',
                                             memo='Memo',
                                             delta=Decimal(25))
        self.request = factory.get(reverse('transactions:detail',
                                           kwargs={'pk': self.tx.pk}))

    def render_response(self, authenticated_user=None):
        if authenticated_user is not None:
            force_authenticate(self.request, user=authenticated_user)
        response = TransactionDetail.as_view()(self.request,
                                               pk=self.tx.pk)
        response.render()
        return response

    def test_access_of_transaction_not_logged_in(self):
        response = self.render_response()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_access_of_transaction_not_owner(self):
        response = self.render_response(self.user2)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_access_of_transaction_correctly(self):
        response = self.render_response(self.user)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(self.tx.pk, content['id'])
        self.assertEqual('2016-08-02', content['date'])
        self.assertEqual('Payee', content['payee'])
        self.assertEqual('Memo', content['memo'])
        self.assertEqual('25.00', content['delta'])
