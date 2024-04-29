from django import forms
from account_module.models import User
from django.core import validators
from django.core.exceptions import ValidationError



class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'نام ', 'class':'form-control'} ),
            'last_name': forms.TextInput(attrs={'placeholder':'نام خانوادگی', 'class':'form-control'} ),
            'avatar': forms.FileInput(attrs={'placeholder':'تصویر', 'class':'form-control'}),
            'address': forms.TextInput(attrs={'placeholder':'آدرس', 'class':'form-control'}),
            'about_user': forms.Textarea(attrs={'placeholder':'درباره من', 'class':'form-control', 'id':'message', 'rows':5}),

        }
                
        labels = {
            'first_name':'نام ',
            'last_name':'نام خانوادگی',
            'avatar':'تصویر پروفایل',
            'address':'آدرس',
            'about_user':'درباره من'
        }



class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(label='رمز عبور فعلی' ,widget=forms.TextInput(attrs={'class':'form-control'}))

    new_password = forms.CharField(label='رمز عبور جدید',widget=forms.PasswordInput(attrs={'class':'form-control'}) , validators=[validators.MaxLengthValidator(100)])

    confirm_password = forms.CharField(label='تایید رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control'}) , validators=[validators.MaxLengthValidator(100)])


    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('رمز عبور مطابقت ندارد')
        


    

