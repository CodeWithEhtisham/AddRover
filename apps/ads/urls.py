from django.urls import path
from .views import AdListView

urlpatterns = [
    path("", AdListView.as_view(), name='customer_ads'),
]
