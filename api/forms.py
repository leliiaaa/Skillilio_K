from django import forms
from .models import Order, Profile, Message
from django.contrib.auth.models import User
from .models import Profile

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'category', 'description', 'budget']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва завдання'}),
            'category': forms.Select(attrs={'class': 'form-select'}), 
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишіть деталі...'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума в гривнях'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_freelance', 'is_remote', 'birth_date', 'country', 'city', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'is_freelance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_remote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
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