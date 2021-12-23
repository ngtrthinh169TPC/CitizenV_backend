from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_id', 'managed_by', 'user', 'permission',
                  'name_of_unit', 'classification', 'entry_permit')
