from django import forms
from .models import Advertisement, Response


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'category']
        widgets = {
                   'title': forms.TextInput(attrs={'placeholder': 'Заголовок'}),
                   'text': forms.Textarea(attrs={'placeholder': 'Текст объявления'}),
        }

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
                   'text': forms.Textarea(attrs={'placeholder': 'Текст отклика'}),
        }
