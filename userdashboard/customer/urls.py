from django.urls import path
from .views import  CustomerDashboardView, AdListView, CustomerLoginView, CustomerLogoutView, CustomerRegisterView

urlpatterns = [
    path('', CustomerLoginView.as_view(), name='login'),
    path('logout', CustomerLogoutView.as_view(), name='logout'),
    path('register', CustomerRegisterView.as_view(), name='register'),
    path("dashboard",CustomerDashboardView.as_view(),name='customer_dashboard'),
    path("ads", AdListView.as_view(), name='customer_ads'),
]
