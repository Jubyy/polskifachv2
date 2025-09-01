from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import UserProfile, ContractorProfile

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "CLIENT")  # CLIENT / CONTRACTOR

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, role=role if role in ["CLIENT","CONTRACTOR","MODERATOR","ADMIN"] else "CLIENT")

        # jeżeli CONTRACTOR – od razu utwórz pusty ContractorProfile
        if role == "CONTRACTOR":
            ContractorProfile.objects.create(
                user=user, display_name=username, city="", description=""
            )

        return Response({"message": "User registered successfully"}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        response = Response({"message": "Login successful"}, status=200)
        response.set_cookie("access", str(refresh.access_token), httponly=True, secure=False, samesite="Lax")
        response.set_cookie("refresh", str(refresh), httponly=True, secure=False, samesite="Lax")
        return response

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = getattr(getattr(request.user, "profile", None), "role", "CLIENT")
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "role": role,
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logged out"}, status=200)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
