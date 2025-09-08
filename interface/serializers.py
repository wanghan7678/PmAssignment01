from rest_framework import serializers
from domain.entities.report import Report


class ReportSerializer(serializers.Serializer):
    positions = serializers.DictField()
    basket = serializers.DictField()
    dates = serializers.ListField()