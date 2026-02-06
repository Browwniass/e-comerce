from rest_framework import serializers


class PaymentCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
