from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    Category, ContractorProfile, Service, Listing, JobRequest,
    Conversation, Message, Review, Report
)
from .serializers import (
    CategorySerializer, ContractorListSerializer, ContractorDetailSerializer,
    ServiceSerializer, ListingSerializer, JobRequestSerializer,
    ConversationSerializer, MessageSerializer, ReviewSerializer,
    ReportSerializer
)
from .permissions import IsAuthenticatedOrReadOnly, IsContractor, IsAdminOrModerator

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrModerator|IsAuthenticatedOrReadOnly]

class ContractorViewSet(viewsets.ModelViewSet):
    queryset = ContractorProfile.objects.all().order_by("-avg_rating","-reviews_count")
    filter_backends = [filters.SearchFilter]
    search_fields = ["display_name","city","description","categories__name"]

    def get_permissions(self):
        if self.action in ["list","retrieve","search"]:
            return [AllowAny()]
        # edycja tylko dla admin/moderator (na MVP)
        return [IsAdminOrModerator()]

    def get_serializer_class(self):
        if self.action in ["list","search"]:
            return ContractorListSerializer
        return ContractorDetailSerializer

    @action(detail=False, methods=["get"])
    def search(self, request):
        q = request.query_params.get("q") or ""
        city = request.query_params.get("city")
        cat = request.query_params.get("category")
        queryset = self.get_queryset()
        if q:
            queryset = queryset.filter(
                Q(display_name__icontains=q) |
                Q(description__icontains=q)
            )
        if city:
            queryset = queryset.filter(city__icontains=city)
        if cat:
            queryset = queryset.filter(categories__slug=cat)
        serializer = ContractorListSerializer(queryset.distinct()[:100], many=True)
        return Response(serializer.data)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsContractor()]

    def perform_create(self, serializer):
        contractor = self.request.user.contractor_profile
        serializer.save(contractor=contractor)

    def perform_update(self, serializer):
        contractor = self.request.user.contractor_profile
        if serializer.instance.contractor != contractor:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Nie możesz edytować cudzej usługi.")
        serializer.save()

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsContractor()]

    def perform_create(self, serializer):
        # Listing musi należeć do Service tego wykonawcy
        contractor = self.request.user.contractor_profile
        service = serializer.validated_data.get("service")
        if service.contractor != contractor:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Nie możesz tworzyć ogłoszeń dla cudzej usługi.")
        serializer.save()

    def perform_update(self, serializer):
        contractor = self.request.user.contractor_profile
        if serializer.instance.service.contractor != contractor:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Nie możesz edytować cudzego ogłoszenia.")
        serializer.save()

class JobRequestViewSet(viewsets.ModelViewSet):
    queryset = JobRequest.objects.all().order_by("-created_at")
    serializer_class = JobRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("created_at")
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ==== Moderacja: zgłoszenia ====
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by("-created_at")
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]  # każdy zalogowany może zgłaszać
        # lista/edycja statusu – moderator/admin
        return [IsAdminOrModerator()]
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
