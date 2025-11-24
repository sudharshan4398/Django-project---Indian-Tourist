from django import forms

class FlightSearchForm(forms.Form):
    TRIP_CHOICES = [('round', 'Round Trip'), ('one_way', 'One Way'), ('multi', 'Multi-City')]
    CLASS_CHOICES = [('economy', 'Economy'), ('business', 'Business')]

    trip_type = forms.ChoiceField(choices=TRIP_CHOICES, widget=forms.RadioSelect)
    origin = forms.CharField(max_length=100)
    destination = forms.CharField(max_length=100)
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    adults = forms.IntegerField(min_value=1, max_value=5)
    children = forms.IntegerField(min_value=0, max_value=3)
    infants = forms.IntegerField(min_value=0, max_value=2)
    flight_class = forms.ChoiceField(choices=CLASS_CHOICES, widget=forms.RadioSelect)


class FlightSearchForm(forms.Form):
    origin = forms.CharField(max_length=100)
    destination = forms.CharField(max_length=100)
    departure_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )
    return_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        required=False,
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )
    adults = forms.IntegerField(min_value=1)
    children = forms.IntegerField(min_value=0)
    infants = forms.IntegerField(min_value=0)
    flight_class = forms.ChoiceField(choices=[('economy', 'Economy'), ('business', 'Business')])