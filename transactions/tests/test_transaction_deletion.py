from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

import datetime
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from transactions.models import Transaction
from transactions.views import TransactionDetail


class TransactionDeletionTests(TestCase):
    def setUp(self):
        factory = APIRequestFactory()
        self.user = User.objects.create(username='user')
        self.user2 = User.objects.create(username='user2')
        self.tx = Transaction.objects.create(user=self.user,
                                             date=datetime.date(2016, 8, 2),
                                             payee='Payee',
                                             memo='Memo',
                                             delta=Decimal(25))
        self.request = factory.delete(reverse('transactions:detail',
                                              kwargs={'pk': self.tx.pk}))

    def render_response(self, authenticated_user=None):
        if authenticated_user is not None:
            force_authenticate(self.request, user=authenticated_user)
        response = TransactionDetail.as_view()(self.request, pk=self.tx.pk)
        response.render()
        return response

    def test_deletion_of_transaction_not_logged_in(self):
        response = self.render_response()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Transaction.objects.count())

    def test_deletion_of_transaction_correctly(self):
        response = self.render_response(self.user)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Transaction.objects.count())
