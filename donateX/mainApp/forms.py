from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# class RegistrationForm(UserCreationForm):
#     # Add any additional fields if needed
#     class Meta:
#         model = CustomUser  # Replace with your user model
#         fields = ('username', 'phone', 'password1', 'password2')  # Include the fields you want in the registration form

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'phone')  # Include the fields you want in the registration form

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)