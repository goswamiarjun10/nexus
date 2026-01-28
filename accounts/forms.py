from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input block w-full bg-gray-200 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white pl-3 py-3',
        'placeholder': 'Password',
    }))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input block w-full bg-gray-200 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white pl-3 py-3',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input block w-full bg-gray-200 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white pl-3 py-3',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input block w-full bg-gray-200 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white pl-3 py-3',
                'placeholder': 'Email address',
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise ValidationError("Passwords do not match")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists. Try to another Email.")
        return email
        
class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EmailLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input block w-full bg-gray-200 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white pl-3 py-3',
        'placeholder': 'Email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input block w-full bg-gray-200 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white pl-3 py-3',
        'placeholder': 'Password',
    }))


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input block w-full bg-gray-100 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white px-4 py-3 text-lg'
