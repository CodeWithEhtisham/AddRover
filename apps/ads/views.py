from django.shortcuts import render
from django.views.generic import TemplateView , View
from .forms import AdForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
# from django.http import HttpResponseRedirect
# Create your views here.


class AdListView(TemplateView):
    template_name = 'ads_list.html'

    def get(self,request):
        return render(request, self.template_name)

class AdCreateView(View):  # Change TemplateView to View
    template_name = 'create_ad.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            form = AdForm(request,request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                form.save()
                print(form.errors)
                messages.success(request, "Ad created successfully")
                return redirect(reverse_lazy('customer_ads'))
            else:
                messages.error(request, "Ad not created, please check the form")
                print(form.errors)
                return render(request, self.template_name, {'form': form})

        except Exception as e:
            messages.error(request, f"Ad not created, {e}")
            print(e)
            return render(request, self.template_name, {'form': form})
