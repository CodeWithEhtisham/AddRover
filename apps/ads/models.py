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
    
    def get_ad_type_display(self):
        # This method returns the display value for the ad_type field
        return dict(self.ad_type_choices).get(self.ad_type, '')


class Week(models.Model):
    start_date = models.DateField(unique=True)
    end_date = models.DateField()

    class Meta:
        db_table = 'week'
        ordering = ['start_date']

    def __str__(self):
        return f"Week {self.start_date} - {self.end_date}"

    def create_weekly_slots(self):
        # Create 4 slots for this week
        for slot_number in range(1, 5):
            Slot.objects.create(week=self, slot_number=slot_number, slot_type='weekly')

class Month(models.Model):
    start_date = models.DateField(unique=True)  # Usually the first day of the month
    end_date = models.DateField()  # Usually the last day of the month

    class Meta:
        db_table = 'month'
        ordering = ['start_date']

    def __str__(self):
        return f"Month {self.start_date.strftime('%B')}"

    def create_monthly_slots(self):
        # Create 4 slots for this month
        for slot_number in range(1, 5):
            Slot.objects.create(month=self, slot_number=slot_number, slot_type='monthly')

class Slot(models.Model):
    SLOT_TYPE_CHOICES = (
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )

    week = models.ForeignKey(Week, on_delete=models.CASCADE, null=True, blank=True, related_name='slots')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True, related_name='slots')
    slot_number = models.PositiveIntegerField()  # 1 to 4
    slot_type = models.CharField(max_length=10, choices=SLOT_TYPE_CHOICES)
    # ad = models.ForeignKey('Ad', on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'slot'
        unique_together = ('week', 'month', 'slot_number')  # Ensures slots are unique in either weekly or monthly context
        ordering = ['slot_number']

    def __str__(self):
        return f"Slot {self.slot_number} ({self.get_slot_type_display()})"