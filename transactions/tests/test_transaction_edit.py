from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

import datetime
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from transactions.models import Transaction
from transactions.views import TransactionDetail


class TransactionEditingTests(TestCase):
    def setUp(self):
        factory = APIRequestFactory()
        self.user = User.objects.create(username='user')
        self.user2 = User.objects.create(username='user2')
        self.tx = Transaction.objects.create(user=self.user,
                                             date=datetime.date(2016, 8, 2),
                                             payee='Payee', memo='Memo',
                                             delta=Decimal(25))
        data = {'date': '2008-08-08', 'payee': 'Payee2', 'memo': 'Memo2',
                'delta': Decimal(-40)}
        self.request = factory.put(
            reverse('transactions:detail', kwargs={'pk': self.tx.pk}), data)

    def render_response(self, authenticated_user=None):
        if authenticated_user is not None:
            force_authenticate(self.request, user=authenticated_user)
        response = TransactionDetail.as_view()(self.request, pk=self.tx.pk)
        response.render()
        return response

    def test_editing_transaction_not_logged_in(self):
        response = self.render_response()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Transaction.objects.count())

    def test_editing_transaction_wrong_owner(self):
        response = self.render_response(self.user2)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Transaction.objects.count())

    def test_editing_transaction_correctly(self):
        response = self.render_response(self.user)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Transaction.objects.count())
        tx = Transaction.objects.all()[0]
        self.assertEqual(self.user, tx.user)
        self.assertEqual(datetime.date(2008, 8, 8), tx.date)
        self.assertEqual('Payee2', tx.payee)
        self.assertEqual('Memo2', tx.memo)
        self.assertEqual(Decimal(-40), tx.delta)
