from django.shortcuts import render
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomerForm,LoginForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class CustomerLoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email_or_username = request.POST.get('email-username')
        password = request.POST.get('password')

        # Check both email and username for authentication
        user = authenticate(request, username=email_or_username, password=password)
        print(user)
        if user is None:
            user = authenticate(request, email=email_or_username, password=password)

        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')  # Redirect to your desired page after login
        else:
            messages.error(request, 'Invalid credentials')

        return render(request, 'login.html')

class CustomerLogoutView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)
    
class CustomerRegisterView(TemplateView):
    template_name ='register.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to success page or login page
            return redirect('login')  # Update with the correct URL name for your login page
        # return redirect('success')
        print(form.errors)
        return render(request,'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

