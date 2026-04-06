from django import forms
from .models import Destination, DestinationReview

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    def clean(self, data, initial=None):
        return data

class DestinationForm(forms.ModelForm):
    gallery = MultipleImageField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        label="Galería de imágenes"
    )

    class Meta:
        model = Destination
        fields = ['title', 'description', 'location', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['rating', 'content']