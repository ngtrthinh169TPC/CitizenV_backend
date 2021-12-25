from django.db.models import Count

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Citizen
from .serializers import CitizenSerializer
from accounts.models import Account


class CitizenAPI(APIView):
    def get(self, request):
        account = Account.objects.filter(user=request.user)
        if account[0].account_id == '000admin':
            citizens = Citizen.objects.all()
        else:
            citizens = Citizen.objects.filter(
                managed_by__account_id__startswith=account[0].account_id)
        serializer = CitizenSerializer(citizens, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = CitizenSerializer(data=request.data)
        account = Account.objects.filter(user=request.user)
        if serializer.is_valid():
            Citizen.objects.create(
                citizen_id=request.data.get('citizen_id'),
                managed_by=account[0],
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
        citizen = Citizen.objects.get(
            citizen_id=request.data.get("citizen_id"))
        serializer = CitizenSerializer(
            citizen, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        citizen = Citizen.objects.get(
            citizen_id=request.data.get("citizen_id"))
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
        gender = (Citizen.objects.values('gender').annotate(
            count=Count('gender')).order_by())
        religious = (Citizen.objects.values('religious').annotate(
            count=Count('religious')).order_by())
        education = (Citizen.objects.values('education').annotate(
            count=Count('education')).order_by())
        return Response(status=200, data={'gender': gender, 'religious': religious, 'education': education})
