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
        Report.objects.create(
            reporter=request.data.get('reporter'),
            completed=request.data.get('completed'),
            account=account,
        )
        account.completed = request.data.get('completed')
        account.save()
        if (request.data.get('completed') == "True"):
            print(account.managed_by)
        return Response(status=201, data={'account_id': account.account_id, 'completed': account.completed})
