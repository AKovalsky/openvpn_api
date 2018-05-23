from django.db import models
from django.utils.crypto import get_random_string

def get_random_string_model():
    return get_random_string(length=12)

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    username = models.CharField(max_length=30, unique=True, default=get_random_string_model)
    discord_username = models.CharField(max_length=255, unique=True, null=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default=get_random_string_model)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    online = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    basename = models.CharField(max_length=30, blank=True)
    csr = models.CharField(max_length=30, blank=True)
    certificate = models.CharField(max_length=30, blank=True)
    key = models.CharField(max_length=30, blank=True)
    serial = models.CharField(max_length=255, blank=True)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

