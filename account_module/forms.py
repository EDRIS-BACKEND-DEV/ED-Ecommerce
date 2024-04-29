from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        validators=[validators.MaxLengthValidator(100), validators.EmailValidator]
    )
    password = forms.CharField(
        max_length=130,
        widget=forms.PasswordInput(),
        validators=[validators.MaxLengthValidator(100)]
        )
    
    confirm_password = forms.CharField(
        max_length=130,
        widget=forms.PasswordInput(),
        validators=[validators.MaxLengthValidator(100)])

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('رمز عبور مطابقت ندارد')



class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        validators=[validators.MaxLengthValidator(100), validators.EmailValidator]
    )

    password = forms.CharField(
        max_length=130,
        widget=forms.PasswordInput(),
        validators=[validators.MaxLengthValidator(100)]
        )
    


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        validators=[validators.MaxLengthValidator(100), validators.EmailValidator]
    )



class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validators.MaxLengthValidator(100)]
        )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validators.MaxLengthValidator(100)])


