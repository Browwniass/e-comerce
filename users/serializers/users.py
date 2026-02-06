from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs.get("refresh_token")
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {"refresh": ["Invalid or expired token."]}
            )
