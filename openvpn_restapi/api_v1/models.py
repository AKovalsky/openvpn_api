from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    online = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate = models.TextField()
    key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)