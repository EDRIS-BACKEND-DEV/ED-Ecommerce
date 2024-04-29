from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from .models import User
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from utils.email_service import send_email

# Create your views here.

class RegisterPageView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'Register_Page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }

        return render(request, 'Register_Page.html', context)


        

    
class LoginView(View):
    
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form':login_form
        }
        return render(request, 'Login_Page.html', context)
    
    def post(self, request):
        login_form = LoginForm(request.POST)

      #checking if the form is valid
        if login_form.is_valid():
            #fetching the data from what the user has signed in
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')

            #checking if the information that the user has signed in equal
            # with the first information he signed in

            user: User = User.objects.filter(email__iexact=user_email).first()

            # if the data information exists
            if user is not None:
 
              #we will give the user an error if he doesnt verify
              #his email code verification

                if not user.is_active:
                    login_form.add_error('email', 'You have not confirmed you\'r email')

                  #now this checks if the users password that he assigned is correct   
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('Home'))
                    else:
                        login_form.add_error('email', 'The Password is incorrect')
                    
            else:
                login_form.add_error('email','The Email or Password is incorrect')
            


        context = {
            'login_form':login_form
        }
        
        return render(request, 'Login_Page.html', context)



class ActivateCodeView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show your user that the account was logged in successfully
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated message before to the user
                ...

        raise Http404





class ForgotPasswordView(View):

    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'Forgot_Password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                
                send_email('| بازیابی کلمه عبور | Password Recovery |',
                 user.email, {'user':user}, 'emails/forgot_password.html')
                return redirect(reverse('login_page'))

                

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'Forgot_Password.html', context)


            




class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()

        #if the email active code werent the same as the one that the user just has passed into.
        #he will get redirected to the login_page instead.
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = ResetPasswordForm()

        context = {
                   'reset_pass_form': reset_pass_form,
                   'user':user,
                   }
        return render(request, 'Reset_Password.html', context)
    
    def post(self, request:HttpRequest, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        if reset_pass_form.is_valid():
            user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        
        if user is None:
            return redirect(reverse('login_page'))
        
        else:
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))
         
        

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
    
  

