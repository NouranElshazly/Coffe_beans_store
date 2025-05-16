from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
 
        ('admin', 'Admin')
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='admin')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Properties for easy checking
    @property
    def is_customer(self):
        return self.user_type == 'customer'
 
    
    @property
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser

    def __str__(self):
        return self.username