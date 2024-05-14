from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    name = models.CharField(max_length=32, default='')

    class Meta:
        db_table = "auth_user_role"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'auth_user_profile'
