from rest_framework import serializers
from .models import Citizen


class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ('citizen_id', 'first_name', 'last_name', 'date_of_birth', 'place_of_birth',
                  'place_of_origin', 'permanent_address', 'temporary_address', 'religious', 'occupation', 'education')
