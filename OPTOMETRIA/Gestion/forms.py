from django import forms
from .models import Pacientes
from django.forms import ModelForm
from django.db import models

#class regEjemplo(forms.ModelForm):
##    class Meta:
#        model=Pacientes
#        fields=["apellidos","nombres"]

class regPaciente(forms.Form):
    apellidos=forms.CharField(max_length=64)
    nombres=forms.CharField(max_length=64)
    
