from django.urls import path
from .views import AdListView , AdCreateView

urlpatterns = [
    path("", AdListView.as_view(), name='customer_ads'),
    path("create/", AdCreateView.as_view(), name='create_ad'),
]
