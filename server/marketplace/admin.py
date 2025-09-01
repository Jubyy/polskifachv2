from django.contrib import admin
from .models import (
    Category, ContractorProfile, Service, Listing, JobRequest,
    Conversation, Message, Review, UserProfile, Report
)

admin.site.register(Category)
admin.site.register(ContractorProfile)
admin.site.register(Service)
admin.site.register(Listing)
admin.site.register(JobRequest)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Report)
