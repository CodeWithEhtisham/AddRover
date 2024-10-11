from django.shortcuts import render
from django.views.generic import TemplateView , View
from .forms import AdForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import Ad
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from .models import Slot, Week, Month
import json

# from django.http import HttpResponseRedirect
# Create your views here.


class AdListView(TemplateView):
    template_name = 'ads_list.html'

    def get(self,request):
        ads = Ad.objects.filter(customer=request.user)
        return render(request, self.template_name, {'ads': ads})

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


class SlotCreateView(TemplateView):
    template_name = 'create_slot.html'

    def get(self,reqeust):
        ads = Ad.objects.filter(customer=reqeust.user)
        return render(reqeust, self.template_name, {'ads': ads})
    
@csrf_exempt
def fetch_slots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        slot_type = data.get('type')  # 'week' or 'month'
        selected_value = data.get('value')  # Example: '2024-W44' for week or '2024-10' for month

        if slot_type == 'week':
            year, week_number = selected_value.split('-W')

            # Convert to the first day of the week (Monday)
            start_date = datetime.strptime(f'{year} {week_number} 1', '%Y %W %w').date()
            end_date = start_date + timedelta(days=6)

            # Check if the week already exists
            week_obj, created = Week.objects.get_or_create(
                start_date=start_date,
                end_date=end_date
            )

            # If it's a newly created week, create 4 slots for the week
            if created:
                week_obj.create_weekly_slots()

            # Retrieve available slots for the week
            slots = week_obj.slots.all()

        elif slot_type == 'month':
            year, month = selected_value.split('-')

            # First day of the month
            start_date = datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d').date()
            # Last day of the month
            end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

            # Check if the month already exists
            month_obj, created = Month.objects.get_or_create(
                start_date=start_date,
                end_date=end_date
            )

            # If it's a newly created month, create 4 slots for the month
            if created:
                month_obj.create_monthly_slots()

            # Retrieve available slots for the month
            slots = month_obj.slots.all()

        # Return available slots
        available_slots = [{
            'slot_number': slot.slot_number,
            'is_available': slot.is_available
        } for slot in slots]

        return JsonResponse({'success': True, 'slots': available_slots})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)