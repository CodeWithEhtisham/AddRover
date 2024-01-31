from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class AdListView(TemplateView):
    template_name = 'ads_list.html'

    def get(self,request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass