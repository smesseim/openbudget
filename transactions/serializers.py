from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="transactions:detail")

    class Meta:
        model = Transaction
        fields = ('url', 'id', 'date', 'payee', 'memo', 'delta')
