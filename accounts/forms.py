from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User

INPUT_CLASSES = (
    'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
    'focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent text-sm'
)


class AccountRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Juan Dela Cruz'}),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'juandelacruz'}),
    )
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'juan@example.com'}),
    )
    contact_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '+63 917 123 4567'}),
    )
    role = forms.ChoiceField(
        choices=User.Role.choices,
        required=True,
        widget=forms.Select(attrs={'class': INPUT_CLASSES}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'username', 'email', 'contact_number', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Enter a strong password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Confirm your password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email address is already registered (BR-01).')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken. Please choose another.')
        return username


class AccountLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter your registered email',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter your password',
        }),
    )


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'contact_number', 'profile_photo')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'username': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'contact_number': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '+63 9XX XXX XXXX'}),
            'profile_photo': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('That email address is already in use by another account (BR-01).')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('That username is already in use by another account.')
        return username