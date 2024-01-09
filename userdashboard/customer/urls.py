from django.urls import path
from .views import  CustomerDashboardView, AdListView

urlpatterns = [
    path("customer/dashboard",CustomerDashboardView.as_view(),name='customer_dashboard'),
    path("customer/ads", AdListView.as_view(), name='customer_ads'),
]
