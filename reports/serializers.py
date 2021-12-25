from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('report_id', 'created_at',
                  'reporter', 'completed', 'account')
