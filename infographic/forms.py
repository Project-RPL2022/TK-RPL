from .models import Infographic
from django.forms import ModelForm
from hotel.models import Hotel, Facility


class GetInfographicForm(ModelForm):
    class Meta:
        model = Infographic
        fields = ['hotel']
    

