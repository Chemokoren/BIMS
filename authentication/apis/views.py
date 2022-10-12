from django.contrib.auth.password_validation import validate_password
from rest_framework import viewsets, serializers, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.apis.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    """A user ViewSet for viewing and editing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterUserAPIView(generics.CreateAPIView):
    """Class based view to register user"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class LogoutView(APIView):
    """You should add refresh token to the blacklisted tokens manually"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)