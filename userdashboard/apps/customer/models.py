from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    phone = models.CharField(max_length=100)
    cnic = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        db_table = 'customers'