from django import forms
from .models import Publication


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        if len(data) > 10:
            raise forms.ValidationError(
                "Puedes subir un máximo de 10 fotografías."
            )

        images = []

        for image in data:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    f"La imagen {image.name} supera los 5 MB."
                )

            if image.content_type not in (
                "image/jpeg",
                "image/png",
                "image/webp",
            ):
                raise forms.ValidationError(
                    "Solo se permiten imágenes JPG, PNG y WebP."
                )

            images.append(
                super().clean(image, initial)
            )

        return images



class PublicationForm(forms.ModelForm):

    images = MultipleImageField(
        required=False,
        label="Fotografías",
        help_text="Puedes añadir hasta 10 fotografías de 5 MB cada una.",
    )

    class Meta:
        model = Publication

        fields = [
            "publication_type",
            "title",
            "description",
            "location",
        ]

        labels = {
            "publication_type": "Tipo de publicación",
            "title": "Título",
            "description": "Descripción",
            "location": "Localización",
        }

        widgets = {
            "publication_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ponle un título a tu aventura",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 7,
                    "placeholder": "Cuéntanos tu aventura...",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: Pirineos, Huesca, España",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["publication_type"].choices = [
            ("", "Selecciona una categoría"),
            ("ROUTE", "Ruta"),
            ("VEHICLE", "Vehículo"),
            ("EXPERIENCE", "Experiencia"),
        ]

        self.fields["location"].required = False

        self.fields["location"].help_text = (
            "Indica dónde tuvo lugar tu aventura. "
            "Este campo es opcional."
        )

    def clean_publication_type(self):
        value = self.cleaned_data["publication_type"]

        if value not in ("ROUTE", "VEHICLE", "EXPERIENCE"):
            raise forms.ValidationError(
                "Selecciona una categoría válida."
            )

        return value
