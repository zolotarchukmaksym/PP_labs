from django import forms
from .models import Technician

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name', 'specialization']
