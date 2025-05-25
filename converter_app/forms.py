from django import forms
from .models import EmailUsers

class EmailUsersForm(forms.ModelForm):
    class Meta:
        model = EmailUsers
        fields = ['email']
