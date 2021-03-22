from space.models import Stories
from django.forms import ModelForm


class StoriesForm(ModelForm):
    class Meta:
        model = Stories
        fields = ('headline', 'category', 'region', 'details')
