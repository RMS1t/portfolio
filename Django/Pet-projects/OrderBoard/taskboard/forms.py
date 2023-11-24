from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import AdvUser

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords don\'t match.')
    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))
        if commit:
            user.save()
        return  user

    class Meta:
        model = AdvUser
        fields = ['login', "username", "email", "pd_agree"]


