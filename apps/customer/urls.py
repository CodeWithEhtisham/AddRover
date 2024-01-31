from django.urls import path
from .views import  CustomerLoginView, CustomerLogoutView, CustomerRegisterView

urlpatterns = [
    path('', CustomerLoginView.as_view(), name='login'),
    path('logout', CustomerLogoutView.as_view(), name='logout'),
    path('register', CustomerRegisterView.as_view(), name='register'),
]
