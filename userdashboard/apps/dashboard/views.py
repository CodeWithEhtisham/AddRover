from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class CustomerDashboardView(TemplateView):

    template_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass