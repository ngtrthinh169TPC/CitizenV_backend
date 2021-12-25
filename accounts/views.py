from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


class AccountAPI(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(data=serializer.data)


class ChildAccountAPI(APIView):
    def get(self, request):
        children_account = Account.objects.filter(
            Q(managed_by__user=request.user))
        serializer = AccountSerializer(children_account, many=True)
        return Response(data=serializer.data)


class EntryPermitAPI(APIView):
    def entry_permit_recursion(self, account):
        accounts = Account.objects.filter(managed_by=account)
        for acc in accounts:
            acc.entry_permit = False
            acc.save()
            self.entry_permit_recursion(acc)

    def patch(self, request):
        account = Account.objects.get(user=request.user)
        account.entry_permit = request.data.get('entry_permit')
        account.save()

        if (request.data.get('entry_permit') == "False"):
            self.entry_permit_recursion(account)

        return Response(status=204)
