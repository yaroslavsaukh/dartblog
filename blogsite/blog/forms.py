from django import forms
from .models import Comment, Post, Email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widget = {
            'name': forms.TextInput(attrs={'class': 'name', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'email'}),
            'content': forms.TextInput(attrs={'class': 'comment'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']
        widget = {
            'email': forms.EmailInput()
        }
        labels = {
            'email': ''
        }
