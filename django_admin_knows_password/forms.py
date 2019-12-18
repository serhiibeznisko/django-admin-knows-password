from django import forms
from django.contrib.auth import get_user_model, password_validation


class ChangePasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password_validation.validate_password(password1, self.instance)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
