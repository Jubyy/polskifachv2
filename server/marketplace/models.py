from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    def __str__(self): return self.name

class ContractorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="contractor_profile")
    display_name = models.CharField(max_length=120)
    city = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    min_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    radius_km = models.PositiveIntegerField(default=20)
    avg_rating = models.FloatField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=50, blank=True)
    categories = models.ManyToManyField(Category, related_name="contractors", blank=True)
    def __str__(self): return self.display_name

class Service(models.Model):
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class Listing(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="listings")
    city = models.CharField(max_length=120)
    coverage_radius_km = models.PositiveIntegerField(default=20)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=[("ACTIVE","ACTIVE"),("PAUSED","PAUSED"),("ARCHIVED","ARCHIVED")], default="ACTIVE")

class JobRequest(models.Model):
    client_name = models.CharField(max_length=120)
    client_email = models.EmailField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="job_requests")
    city = models.CharField(max_length=120)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE, related_name="conversations")
    client_email = models.EmailField()
    client_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=16, choices=[("CLIENT","CLIENT"),("CONTRACTOR","CONTRACTOR")])
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    author_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
