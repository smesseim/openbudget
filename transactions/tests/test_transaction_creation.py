from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

import datetime
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from transactions.models import Transaction
from transactions.views import TransactionList


class TransactionCreationTests(TestCase):
    def setUp(self):
        factory = APIRequestFactory()
        self.user = User.objects.create(username='user')
        data = {
            'date': '2016-08-02',
            'payee': 'Payee',
            'memo': 'Memo',
            'delta': Decimal(25),
        }
        self.request = factory.post(reverse('transactions:list'), data=data)

    def render_response(self, authenticated_user=None):
        if authenticated_user is not None:
            force_authenticate(self.request, user=authenticated_user)
        response = TransactionList.as_view()(self.request)
        response.render()
        return response

    def test_creation_of_transaction_not_logged_in(self):
        response = self.render_response()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(0, Transaction.objects.count())

    def test_creation_of_transaction_correctly(self):
        response = self.render_response(self.user)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Transaction.objects.count())
        tx = Transaction.objects.all()[0]
        self.assertEqual(self.user, tx.user)
        self.assertEqual(datetime.date(2016, 8, 2), tx.date)
        self.assertEqual('Payee', tx.payee)
        self.assertEqual('Memo', tx.memo)
        self.assertEqual(Decimal(25), tx.delta)
