from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class AdListView(TemplateView):
    template_name = 'ads_list.html'

    def get(self,request):
        return render(request, self.template_name)

class AdCreateView(TemplateView):
    template_name = 'create_ad.html'

    def post(self,request):
        return render(request, self.template_name)
