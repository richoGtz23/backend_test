from rest_framework import serializers


class PayloadSerializer(serializers.Serializer):
    status = serializers.CharField(read_only=True)
    num_in_english = serializers.CharField(required=True, max_length=1000)
