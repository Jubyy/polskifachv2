from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ContractorViewSet, ServiceViewSet, ListingViewSet,
    JobRequestViewSet, ConversationViewSet, MessageViewSet, ReviewViewSet,
    ReportViewSet
)
from .auth_views import RegisterView, LoginView, MeView, LogoutView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"contractors", ContractorViewSet, basename="contractors")
router.register(r"services", ServiceViewSet, basename="services")
router.register(r"listings", ListingViewSet, basename="listings")
router.register(r"jobs", JobRequestViewSet, basename="jobs")
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"reports", ReportViewSet, basename="reports")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
