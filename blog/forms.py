from django import forms
from .models import Post, Comment

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    """Permite subir múltiples imágenes"""
    def clean(self, data, initial=None):
        if not data:
            return []
        return [super(MultipleImageField, self).clean(f) for f in data]

class PostForm(forms.ModelForm):
    images = MultipleImageField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        label="Imágenes"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario aquí...'
            }),
        }