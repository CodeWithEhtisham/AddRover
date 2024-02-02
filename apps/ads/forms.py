from django.forms import ModelForm
from apps.ads.models import Ad

class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'ad_type', 'duration', 'video']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        ad = super().save(commit=False)
        ad.customer = self.request.user
        if commit:
            ad.save()
        return ad