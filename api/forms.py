from django import forms
from .models import Order, Profile, Message
from django.contrib.auth.models import User
from .models import Profile

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'category', 'description', 'requirements', 'budget'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва завдання'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опишіть суть завдання...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Наприклад: Знання Python, досвід з Django, вміння працювати з API...'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логін'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'languages', 'is_freelance', 'is_remote', 'birth_date', 'country', 'city'] # <--- Додали 'languages'
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: Англійська (B2), Українська (Рідна)'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'is_freelance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_remote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Напишіть повідомлення...'
            }),
        }        