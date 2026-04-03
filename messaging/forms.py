from django import forms

class ContactSellerForm(forms.Form):
    name = forms.CharField(max_length=100, label="Tu nombre", required=True)
    email = forms.EmailField(label="Tu email de contacto", required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Mensaje", required=True)