from rest_framework import serializers
from .models import (
    Category, ContractorProfile, Service, Listing, JobRequest,
    Conversation, Message, Review, UserProfile, Report
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id","rating","comment","author_name","created_at"]

class ContractorListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = ContractorProfile
        fields = ["id","display_name","city","description","min_rate","radius_km","avg_rating","reviews_count","phone","categories"]

class ContractorDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = ContractorProfile
        fields = ["id","display_name","city","description","min_rate","radius_km","avg_rating","reviews_count","phone","categories","reviews"]

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"

class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id","sender","body","created_at","conversation"]

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ["id","contractor","client_email","client_name","created_at","messages"]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["role"]

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id","reporter","target_type","target_id","reason","status","created_at"]
        read_only_fields = ["reporter","status","created_at"]
