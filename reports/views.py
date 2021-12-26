from functools import partial
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Report

from accounts.models import Account
from accounts.serializers import AccountSerializer


class ReportAPI(APIView):
    def post(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission != "B1"):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        Report.objects.create(
            reporter=request.data.get('reporter'),
            completed=request.data.get('completed'),
            account=account,
        )
        account.completed = request.data.get('completed')
        account.save()
        manager_acc = account.managed_by
        while (manager_acc != None):
            total = Account.objects.filter(managed_by=manager_acc).count()
            completed = Account.objects.filter(
                managed_by=manager_acc, completed=True).count()
            if (total == completed):
                manager_acc.completed = True
                manager_acc.save()
            else:
                manager_acc.completed = False
                manager_acc.save()
            manager_acc = manager_acc.managed_by
        return Response(status=201, data={'account_id': account.account_id, 'completed': account.completed})
