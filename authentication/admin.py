from django.contrib import admin
from .models import UserProfile, UserRole
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserRole)
