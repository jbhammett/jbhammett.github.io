from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django import forms


CATEGORY_CHOICES = [
    ('', '--------'),
    ('FAMILIES', 'Familes'),
    ('INDIVIDUALS', 'Individuals'),
    ('PETS', 'Pets')
]


class NewPostForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        "class": "form-control"
        }))
    content = forms.CharField(label="Description",
                              widget=forms.Textarea(attrs={
                                     "class": "form-control"
                                     }))
    video = forms.FileField(label="Video", validators=[
                FileExtensionValidator(allowed_extensions=["mp4"])
                ])
    category = forms.ChoiceField(label="Category",
                                 choices=CATEGORY_CHOICES, required=False)
