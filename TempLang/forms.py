from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.forms.fields import EmailField
from .models import Todo
from django import forms

class UserWithEmailCreationForm(UserCreationForm):
    email = EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class TodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ['task', 'completed']