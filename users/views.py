from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
# from rest_framework.views import APIView

from .serializers import UserSerializer
from accounts.models import Account


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        creator = Account.objects.get(
            account_id=request.data.get('creator_id'))
        user = User.objects.create_user(username=request.data.get(
            'username'), password=request.data.get('password'))
        token = Token.objects.create(user=user)
        account = Account.objects.create(
            account_id=request.data.get('account_id'),
            managed_by=creator,
            user=user,
            permission=next_permission(creator.permission),
            # permission=new_permission,
            name_of_unit=request.data.get('name_of_unit'), classification=request.data.get('classification'), entry_permit=request.data.get('entry_permit'))
        return Response(status=201, data={'token': token.key, 'user_id': user.pk, 'username': user.username, 'new_account': account.account_id})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(status=200, data={
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
