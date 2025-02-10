from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django import forms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
        ]
    
    widgets = {
        "username": forms.TextInput(attrs={"required":True, "autofocus": True}),
        "email": forms.EmailInput(attrs={"required":True}),
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("An account with that email already exists.")
        return email
    
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_input(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = CustomUser.objects.filter(username=username)

        if not user.exists():
            raise forms.ValidationError("The username or password did not match, try again.")
        
        else:
            password_match = user.first().check_password(password)
            if not password_match:
                raise forms.ValidationError("The username or password did not match, try again.")
            
            return self.cleaned_data