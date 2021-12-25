from rest_framework import serializers
from .models import Citizen


class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ('object_id', 'citizen_id', 'full_name', 'gender', 'date_of_birth', 'place_of_birth',
                  'place_of_origin', 'permanent_address', 'temporary_address', 'religious', 'occupation', 'education', 'created_at')
