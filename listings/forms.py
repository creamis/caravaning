from django import forms
from .models import Listing, Review

class MultipleFileInput(forms.FileInput):
    """Widget que permite la selección de múltiples archivos."""
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    """Campo de formulario que permite múltiples imágenes."""
    def clean(self, data, initial=None):
        # El widget nos dará una lista de archivos. Simplemente la devolvemos.
        # La vista se encargará de procesar y validar cada archivo individualmente.
        return data

class ListingForm(forms.ModelForm):
    images = MultipleImageField(
        required=False,
        # Usamos nuestro widget personalizado que sí permite múltiples archivos.
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        label="Imágenes"
    )
 
    class Meta:
        model = Listing
        fields = [
            'seller_type',
            'title',
            'description',
            'price',
            'listing_type',
            'category',
            'location',
            'is_available',
            'year',
            'seats',
            'berths',
            'mileage',
            'fuel_type',
            'transmission',
            'length',
            'weight',
            'has_bathroom',
            'has_shower',
            'has_kitchen',
            'has_heating',
            'has_air_conditioning',
            'pets_allowed',
            'has_solar_panels',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'seller_type': forms.Select(attrs={'class': 'form-select'}),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(),
            'has_bathroom': forms.CheckboxInput(),
            'has_shower': forms.CheckboxInput(),
            'has_kitchen': forms.CheckboxInput(),
            'has_heating': forms.CheckboxInput(),
            'has_air_conditioning': forms.CheckboxInput(),
            'pets_allowed': forms.CheckboxInput(),
            'has_solar_panels': forms.CheckboxInput(),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Cuéntanos tu experiencia...', 'class': 'form-control'}),
            'rating': forms.Select(choices=[(i, f"{i} {'Estrella' if i==1 else 'Estrellas'}") for i in range(5, 0, -1)], attrs={'class': 'form-select'}),
        }