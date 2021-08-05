from builtins import super

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Assets, Profile, Address

User = get_user_model()
FORM_VALIDATION_OPTIONS = 0


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'full_name'
        )

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """a form for updating users. includes all the fields on the user, but replaces the password field with admin's password hash display """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'email@',
        'class': 'form-control'

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'INSERT PASSWORD'
    }))


class AssetForm(forms.ModelForm):
    price = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount ',
        'class': 'form-control'
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'name ',
        'class': 'form-control'
    }))
    percentage = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'percentage ',
        'class': 'form-control'
    }))
    picture = forms.ImageField(widget=forms.FileInput(attrs={
        'placeholder': 'picture ',
        'class': 'form-control'
    }))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'your description',
            "cols": 50,
            'rows': 4
        }
    ))

    class Meta:
        model = Assets
        fields = [
            'price',
            'name',
            'description',
            'percentage',
            'picture'

        ]


class TransferForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount ',
        'class': 'form-control'

    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'email@',
        'class': 'form-control'

    }))


class CheckoutForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount ',
        'class': 'form-control'

    }))
    investment_durations = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'period',
        'class': 'form-control'

    }))



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'email@',
        'class': 'form-control'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'FULL NAME',
        'class': 'form-control'})),

    class Meta:
        model = User
        fields = ['full_name', 'email']


class ProfileUpDateForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'wallet address',
        'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['address']


class withdrawalForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount ',
        'class': 'form-control'

    }))
    address = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control ',
        'placeholder': 'select wallet'
    }), queryset=Profile.objects.all(), to_field_name="address")


class DepositForm(forms.Form):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount ',
        'class': 'form-control '
    }))


class AddressForm(forms.Form):
    address = forms.CharField()

    class Meta:
        model = Address
        fields = ['address']



