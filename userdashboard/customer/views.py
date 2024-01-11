from django.shortcuts import render
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

class CustomerLoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
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

class CustomerLogoutView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)
    
class CustomerRegisterView(TemplateView):
    template_name ='register.html'

    def get(self, request):
        return render(request, self.template_name)

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

class CustomerDashboardView(TemplateView):

    template_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass

class AdListView(TemplateView):
    template_name = 'ads_list.html'

    def get(self,request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass