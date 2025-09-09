from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    positions = serializers.DictField()
    basket = serializers.DictField()
    dates = serializers.ListField()