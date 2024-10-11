from django.urls import path
from .views import AdListView , AdCreateView,SlotCreateView,fetch_slots
urlpatterns = [
    path("", AdListView.as_view(), name='customer_ads'),
    path("upload", AdCreateView.as_view(), name='create_ad'),
    path("create/slot", SlotCreateView.as_view(), name='create_slot'),
    path('fetch-slots/', fetch_slots, name='fetch_slots'),
]
