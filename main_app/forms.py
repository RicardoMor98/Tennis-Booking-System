from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Booking
        fields = ['date']
