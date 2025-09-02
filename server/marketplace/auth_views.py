from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, ContractorProfile

# --- Cookies JWT ---
# W DEV (DEBUG=True) przeglądarki często blokują Secure bez HTTPS – wtedy ustawiamy secure=False,
# w PROD (DEBUG=False) MUSI być secure=True i SameSite=None (bo front i API są na różnych domenach).
COOKIE_SETTINGS = dict(
    httponly=True,
    secure=not settings.DEBUG,   # PROD=True, DEV=False
    samesite="None" if not settings.DEBUG else "Lax",
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "CLIENT")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(
            user=user,
            role=role if role in ["CLIENT", "CONTRACTOR", "MODERATOR", "ADMIN"] else "CLIENT"
        )
        if role == "CONTRACTOR":
            ContractorProfile.objects.create(user=user, display_name=username, city="", description="")
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
        access = refresh.access_token

        resp = Response({"message": "Login successful"}, status=200)
        resp.set_cookie("access", str(access), **COOKIE_SETTINGS)
        resp.set_cookie("refresh", str(refresh), **COOKIE_SETTINGS)
        return resp

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

class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.COOKIES.get("refresh")
        if not token:
            return Response({"error": "No refresh token"}, status=401)

        try:
            refresh = RefreshToken(token)
            access = refresh.access_token
        except Exception:
            return Response({"error": "Invalid refresh"}, status=401)

        resp = Response({"message": "refreshed"}, status=200)
        resp.set_cookie("access", str(access), **COOKIE_SETTINGS)
        return resp

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resp = Response({"message": "Logged out"}, status=200)
        resp.delete_cookie("access")
        resp.delete_cookie("refresh")
        return resp
