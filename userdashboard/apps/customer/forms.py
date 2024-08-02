from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class LoginForm(forms.Form):
    email_or_username = forms.CharField(label="Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)

class CustomerForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'email', 'password1','password2', 'phone', 'cnic', 'address']

        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_cnic(self):
        cnic = self.cleaned_data['cnic']
        if len(cnic) != 15 or cnic[5] != '-' or cnic[13] != '-':
            raise forms.ValidationError('Invalid CNIC format. Please use the format: 00000-0000000-0')
        return cnic
