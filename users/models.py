from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    username=None  # Disable username field
    email = models.EmailField(unique=True)  # Use email as unique identifier
    phone_number= models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = []  # No required fields other than email
    
    objects = CustomUserManager()  # Use custom user manager
    
    def __str__(self):
        return self.email
    
