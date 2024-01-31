from django.urls import path
from .views import  CustomerDashboardView

urlpatterns = [
    path("",CustomerDashboardView.as_view(),name='customer_dashboard'),
]
