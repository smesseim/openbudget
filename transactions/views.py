from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import generics, permissions

from .models import Transaction
from .permissions import IsOwner
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


@login_required
def app(request):
    return render(request, 'transactions/main.html')
