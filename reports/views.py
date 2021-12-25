from functools import partial
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Report

from accounts.models import Account
from accounts.serializers import AccountSerializer


class ReportAPI(APIView):
    def post(self, request):
        account = Account.objects.filter(user=request.user)
        Report.objects.create(
            reporter=request.data.get('reporter'),
            completed=request.data.get('completed'),
            account=account[0],
        )
        serializer = AccountSerializer(
            account[0], request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
