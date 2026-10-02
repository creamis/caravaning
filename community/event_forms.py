from django import forms
from django.utils import timezone

from .models import Publication, CommunityEvent


class EventProposalForm(forms.Form):
    cover_image = forms.ImageField(
        label="Imagen de portada",
        required=True,
        help_text="JPG, PNG o WebP. Máximo 5 MB.",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": "image/jpeg,image/png,image/webp",
            }
        ),
    )

    def clean_cover_image(self):
        image = self.cleaned_data["cover_image"]

        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "La imagen no puede superar los 5 MB."
            )

        if image.content_type not in (
            "image/jpeg",
            "image/png",
            "image/webp",
        ):
            raise forms.ValidationError(
                "Solo se admiten imágenes JPG, PNG y WebP."
            )

        return image

    title = forms.CharField(
        label="Nombre del evento",
        max_length=180,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej.: Quedada camper en la Sierra de Cazorla",
        }),
    )

    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 6,
            "placeholder": "Cuéntanos qué tienes organizado...",
        }),
    )

    location = forms.CharField(
        label="Localización",
        max_length=180,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej.: Cazorla, Jaén",
        }),
    )

    starts_at = forms.DateField(
        label="Fecha de la quedada",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "form-control",
            },
        ),
        input_formats=["%Y-%m-%d"],
    )

    start_time = forms.TimeField(
        label="Hora de inicio",
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={
                "type": "time",
                "class": "form-control",
            },
        ),
        input_formats=["%H:%M"],
    )

    capacity = forms.IntegerField(
        label="Número máximo de participantes",
        min_value=1,
        required=False,
        help_text="Déjalo vacío si no hay límite de plazas.",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Ej.: 25",
        }),
    )

    def clean_starts_at(self):
        event_date = self.cleaned_data["starts_at"]

        if event_date < timezone.localdate():
            raise forms.ValidationError(
                "La fecha de la quedada no puede ser anterior a hoy."
            )

        return event_date

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get("starts_at")
        event_time = cleaned_data.get("start_time")

        if event_date and event_time:
            event_datetime = timezone.make_aware(
                __import__("datetime").datetime.combine(
                    event_date, event_time
                ),
                timezone.get_current_timezone(),
            )

            if event_datetime <= timezone.now():
                self.add_error(
                    "start_time",
                    "La fecha y hora deben ser futuras.",
                )

        return cleaned_data
