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
            managed_by=request.data.get('account_id'))
        serializer = AccountSerializer(children_account, many=True)
        return Response(data=serializer.data)
