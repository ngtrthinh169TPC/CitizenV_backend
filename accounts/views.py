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
            managed_by__user=request.user)
        serializer = AccountSerializer(children_account, many=True)
        return Response(status=200, data=serializer.data)

    def patch(self, request):
        account = Account.objects.get(
            account_id=request.data.get('account_id'))
        account.name_of_unit = request.data.get('name_of_unit')
        account.classification = request.data.get('classification')
        account.save()
        return Response(status=204)


class ChildofChildAccountAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        requested_acc = request.data.get('account_id')
        if (requested_acc.startswith(account.account_id)):
            children_account = Account.objects.filter(
                managed_by__account_id=requested_acc)
            serializer = AccountSerializer(children_account, many=True)
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=400)


class EntryPermitAPI(APIView):
    def entry_permit_recursion(self, account):
        accounts = Account.objects.filter(managed_by=account)
        for acc in accounts:
            acc.entry_permit = False
            acc.save()
            self.entry_permit_recursion(acc)

    def patch(self, request):
        account = Account.objects.get(
            account_id=request.data.get('account_id'))
        account.entry_permit = request.data.get('entry_permit')
        account.save()

        if (request.data.get('entry_permit') == "False"):
            accounts = Account.objects.filter(
                account_id__startswith=request.data.get('account_id'))
            for acc in accounts:
                acc.entry_permit = False
                acc.save()

        return Response(status=204)


class ProgressAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        total = Account.objects.filter(managed_by=account)
        completed = total.filter(completed=True).count()
        return Response(status=200, data={'total': total.count(), 'completed': completed})


class AccountManagedAPI(APIView):
    def get(self, request):
        pass
