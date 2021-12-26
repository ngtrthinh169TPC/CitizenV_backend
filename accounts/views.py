from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


class ChildAccountAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission == "B2"):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        children_account = Account.objects.filter(
            managed_by__user=request.user).order_by('account_id')
        serializer = AccountSerializer(children_account, many=True)
        return Response(status=200, data=serializer.data)

    def patch(self, request):
        current_acc = Account.objects.get(user=request.user)
        if (current_acc.permission == "B2"):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        accounts = Account.objects.filter(managed_by=current_acc)
        print(accounts)
        account = get_object_or_404(
            accounts, account_id=request.data.get('account_id'))
        serializer = AccountSerializer(
            account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChildofChildAccountAPI(APIView):
    def post(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission.startswith("B")):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        if (account.account_id == "000admin"):
            accounts = Account.objects.all()
        else:
            accounts = Account.objects.filter(
                account_id__startswith=account.account_id)
        requested = get_object_or_404(
            accounts, account_id=request.data.get('account_id'))
        children = Account.objects.filter(
            managed_by=requested).order_by('account_id')
        serializer = AccountSerializer(children, many=True)
        return Response(status=200, data=serializer.data)


class EntryPermitAPI(APIView):
    def entry_permit_recursion(self, account):
        accounts = Account.objects.filter(managed_by=account)
        for acc in accounts:
            acc.entry_permit = False
            acc.save()
            self.entry_permit_recursion(acc)

    def patch(self, request):
        current_acc = Account.objects.get(user=request.user)
        if (current_acc.permission == "B2"):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        accounts = Account.objects.filter(managed_by=current_acc)
        account = get_object_or_404(
            accounts, account_id=request.data.get('account_id'))
        account.entry_permit = request.data.get('entry_permit')
        account.save()

        if (request.data.get('entry_permit') == "False"):
            accounts = Account.objects.filter(
                account_id__startswith=request.data.get('account_id'))
            for acc in accounts:
                if (acc.entry_permit == True):
                    acc.entry_permit = False
                    acc.save()

        return Response(status=200, data={'account': account.account_id, 'entry_permit': account.entry_permit})


class ProgressAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission.startswith("B")):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        total = Account.objects.filter(managed_by=account)
        completed = total.filter(completed=True).count()
        return Response(status=200, data={'total': total.count(), 'completed': completed})


class AncestorAccountAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)

        ancestors = {}
        finding = account.managed_by
        while (finding):
            ancestors[finding.permission] = {
                finding.name_of_unit, finding.account_id}
            finding = finding.managed_by

        return Response(status=200, data=ancestors)
