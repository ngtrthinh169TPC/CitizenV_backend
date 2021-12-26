from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from accounts.models import Account
from accounts.serializers import AccountSerializer


def next_permission(permission):
    switcher = {
        "A1": Account.a2,
        "A2": Account.a3,
        "A3": Account.b1,
    }
    return switcher.get(permission, Account.b2)


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        creator = Account.objects.get(user=request.user)
        if (creator.permission == "B2"):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(username=request.data.get(
            'username'), password=request.data.get('password'))
        token = Token.objects.create(user=user)
        if (creator.account_id == "000admin"):
            new_account_id = request.data.get('account_id')
        else:
            new_account_id = creator.account_id + \
                request.data.get('account_id')
        account = Account.objects.create(
            account_id=new_account_id,
            managed_by=creator,
            user=user,
            permission=next_permission(creator.permission),
            name_of_unit=request.data.get('name_of_unit'),
        )
        if request.data.get('classification'):
            account.classification = request.data.get('classification')
            account.save()
        if request.data.get('entry_permit'):
            account.entry_permit = request.data.get('entry_permit')
            account.save()
        if (account.permission == "B2"):
            account.completed = True
            account.save()
        return Response(status=201, data={'username': user.username, 'account_id': account.account_id})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        account = user.account
        return Response(status=200, data={
            'token': token.key,
            'account_id': account.account_id,
            'permission': account.permission,
            'name_of_unit': account.name_of_unit,
            'classification': account.classification,
            'entry_permit': account.entry_permit,
            'completed': account.completed,
        })


class WhoAmI(APIView):
    def get(self, request):
        account = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(account, many=True)
        return Response(status=200, data=serializer.data)
