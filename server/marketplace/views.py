from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, ContractorProfile, Service, Listing, JobRequest, Conversation, Message, Review
from .serializers import (
    CategorySerializer, ContractorListSerializer, ContractorDetailSerializer,
    ServiceSerializer, ListingSerializer, JobRequestSerializer,
    ConversationSerializer, MessageSerializer, ReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

class ContractorViewSet(viewsets.ModelViewSet):
    queryset = ContractorProfile.objects.all().order_by("-avg_rating","-reviews_count")
    filter_backends = [filters.SearchFilter]
    search_fields = ["display_name","city","description","categories__name"]

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

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class JobRequestViewSet(viewsets.ModelViewSet):
    queryset = JobRequest.objects.all().order_by("-created_at")
    serializer_class = JobRequestSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("created_at")
    serializer_class = MessageSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
