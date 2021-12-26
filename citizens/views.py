from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Citizen
from .serializers import CitizenSerializer
from accounts.models import Account


class CitizenAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        if account.account_id == '000admin':
            citizens = Citizen.objects.all()
        else:
            citizens = Citizen.objects.filter(
                managed_by__account_id__startswith=account.account_id)
        serializer = CitizenSerializer(citizens, many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission.startswith("A")):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        serializer = CitizenSerializer(data=request.data)
        if serializer.is_valid():
            Citizen.objects.create(
                citizen_id=request.data.get('citizen_id'),
                managed_by=account,
                full_name=request.data.get('full_name'),
                gender=request.data.get('gender'),
                date_of_birth=request.data.get('date_of_birth'),
                place_of_birth=request.data.get('place_of_birth'),
                place_of_origin=request.data.get('place_of_origin'),
                permanent_address=request.data.get('permanent_address'),
                temporary_address=request.data.get('temporary_address'),
                religious=request.data.get('religious'),
                occupation=request.data.get('occupation'),
                education=request.data.get('education')
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission.startswith("A")):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        citizen = Citizen.objects.get(
            object_id=request.data.get("object_id"))
        serializer = CitizenSerializer(
            citizen, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission.startswith("A")):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        citizen = Citizen.objects.get(
            object_id=request.data.get("object_id"))
        citizen.delete()
        return Response(status=204)


# class CitizenAgesAPI(APIView):
#     def get(self, request):
#         arr = [
#             {"0-10": 5},
#             {"11-20": 6},
#         ]
#         return Response(data=arr)


class CitizenStatisticAPI(APIView):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        if (account.permission == "B2"):
            return Response(status=401, data={'detail': "Your account does not have access to this."})

        if (account.account_id == "000admin"):
            citizens = Citizen.objects.all()
        else:
            citizens = Citizen.objects.filter(
                managed_by__account_id__startswith=account.account_id)
        gender = citizens.values('gender').annotate(
            count=Count('gender')).order_by()
        religious = citizens.values('religious').annotate(
            count=Count('religious')).order_by()
        education = citizens.values('education').annotate(
            count=Count('education')).order_by()
        return Response(status=200, data={'gender': gender, 'religious': religious, 'education': education})


class FilterCitizenAPI(APIView):
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
        if requested.account_id == '000admin':
            citizens = Citizen.objects.all().order_by('citizen_id')
        else:
            citizens = Citizen.objects.filter(
                managed_by__account_id__startswith=requested.account_id).order_by('citizen_id')
        serializer = CitizenSerializer(citizens, many=True)
        return Response(status=200, data=serializer.data)
