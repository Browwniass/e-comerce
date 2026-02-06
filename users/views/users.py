from rest_framework import status, permissions, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import AuthException
from users.serializers.users import LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"error": "access_token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy, name="google-oauth2", redirect_uri=None  # ВАЖНО
        )

        try:
            user = backend.do_auth(access_token=access_token)
        except AuthException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            return Response(
                {"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
