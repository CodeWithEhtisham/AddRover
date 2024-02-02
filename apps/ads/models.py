# ads/models.py

from django.db import models
from apps.customer.models import Customer  # Import the Customer model

class Ad(models.Model):
    ad_type_choices = (
        (1, 'CPM'),
        (2, 'Regular'),
    )
    title = models.CharField(max_length=100)
    ad_type = models.IntegerField(choices=ad_type_choices)
    duration = models.TimeField()
    video = models.FileField(upload_to='videos/')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Reference the Customer model

    class Meta:
        db_table = 'ad'

    def __str__(self):
        return self.title
