from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.users import LogoutSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
