from .models import Employee
from django.forms import ModelForm
from django import forms



class EmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={
        'Class':'nameField',
        'id':'nameField',
        'placeholder': 'Name'}))
    point = forms.FloatField(widget = forms.NumberInput(attrs={
        'Class':'pointField',
        'id':'pointField',
        'placeholder': 'Point Index'}))
    phone = forms.CharField(max_length = 10, widget = forms.TextInput(attrs={
        'Class':'phoneField',
        'id':'phoneField',
        'placeholder': 'Phone Number (XXXXXXXXXX)'}))
    class Meta:
        model = Employee
        fields = "__all__"

    