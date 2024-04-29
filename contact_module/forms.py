from django import forms
from .models import ContactUs


class ContactPageForm(forms.Form):
    Name_and_Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'نام و نام خانوادگی', 'class':'form-control'}), label=' نام و نام خانوادگی ', error_messages={'required':'لطفآ نام و نام خانوادگی خود را وارد کنید'})
    Email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={'placeholder':'ایمیل', 'class':'form-control'}))
    title = forms.CharField(label='عنوان', widget=forms.TextInput(attrs={'placeholder':'عنوان', 'class':'form-control'}))
    Message = forms.CharField(label='متن پیام', widget=forms.Textarea(attrs={'placeholder':'عنوان', 'class':'form-control', 'id':'message'}))


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['Email', 'Name_and_Surname', 'title', 'Message']
        
        widgets = {
            'Email':forms.TextInput(attrs={'placeholder':'ایمیل', 'class':'form-control'}),
            'Name_and_Surname': forms.TextInput(attrs={'placeholder':'نام و نام خانوادگی', 'class':'form-control'} ),
            'title': forms.TextInput(attrs={'placeholder':'عنوان', 'class':'form-control'}),
            'Message': forms.Textarea(attrs={'placeholder':'پیام', 'class':'form-control', 'id':'message'}),
        }
                
        labels = {
            'Name_and_Surname':'نام و نام خانوادگی',
            'Email':'ایمیل',
            'title':'عنوان',
            'Message':'پیام',
        }

        error_messages = {
            'Name_and_Surname':{
                'required':'لطفآ نام و نام خانوادگی خود را وارد کنید'
            }
        }




# class UserProfileForm(forms.Form):
#     user_profile = forms.FileField()


class ProfileForm(forms.Form):
    user_image = forms.ImageField()
