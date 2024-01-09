from django.shortcuts import render
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['email']  # Assuming email is used as the username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired page after login
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

class CustomerDashboardView(TemplateView):

    template_name = 'customer_dashboard.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass

class AdListView(TemplateView):
    template_name = 'ad_list.html'

    def get(self,request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass