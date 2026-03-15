from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.utils import api_response


# --------------------------------------------------
# LOGIN
# --------------------------------------------------
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return api_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Invalid credentials",
                general_errors=[str(e)]
            )
        except serializers.ValidationError:
            return api_response(
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

        return api_response(
            status=status.HTTP_200_OK,
            message="Login successful",
            data=serializer.validated_data
        )


# --------------------------------------------------
# REFRESH TOKEN
# --------------------------------------------------
class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return api_response(
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

        return api_response(
            status=status.HTTP_200_OK,
            message="Token refreshed",
            data=serializer.validated_data
        )


# --------------------------------------------------
# VERIFY TOKEN
# --------------------------------------------------
class VerifyTokenView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return api_response(
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

        return api_response(
            status=status.HTTP_200_OK,
            message="Token is valid"
        )