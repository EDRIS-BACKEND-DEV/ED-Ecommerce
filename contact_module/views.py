from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactPageForm, ContactUsModelForm, ProfileForm
from .models import ContactUs, UserProfile
from django.views import View
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
from sitesettings_module.models import SiteSettings

# Create your views here.


#FormView

# class ContactUsView(FormView):
    
#     template_name = 'Contact/contact-us.html'
#     form_class = ContactUsModelForm
#     success_url = '/contact/'

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
    

#CreateView
    

class ContactUsView(CreateView):
    
    template_name = 'Contact/contact-us.html'
    form_class = ContactUsModelForm
    success_url = '/contact/'

    def get_context_data(self, **kwargs: Any):
         context = super().get_context_data(**kwargs)
         settings: SiteSettings = SiteSettings.objects.filter(is_main_setting=True).first()
         context['settings'] = settings

         return context  





# #FILES
    
def store_file(file):
     with open('temp/image.jpg', 'wb+') as dest:
          for chunk in file.chunks():
               dest.write(chunk)
    
# class CreateProfileView(View):
     
#      def get(self, request):
#           form = UserProfileForm()
#           return render(request, 'Contact/create-profile.html')
     
#      def post(self, request):
#           submitted_file = UserProfileForm(request.POST, request.FILES)

#           if submitted_file.is_valid():
#                # store_file(request.FILES['profile'])
#               profile = UserProfileModels(images=request.FILES['user_profile'])
#               profile.save()
#               return redirect('/contact/create-profile')
  
#           return render(request, 'Contact/create-profile.html', {'form':submitted_file})



    
# def store_file(file):
#     with open('temp/image.jpg', "wb+") as dest:
#         for chunk in file.chunks():
#             dest.write(chunk)


# class CreateProfileView(View):
#     def get(self, request):
#         form = ProfileForm()
#         return render(request, 'Contact/create-profile.html', {
#             'form': form
#         })

#     def post(self, request):
#         submitted_form = ProfileForm(request.POST, request.FILES)

#         if submitted_form.is_valid():
#             # store_file(request.FILES['profile'])
#             profile = UserProfile(image=request.FILES["user_image"])
#             profile.save()
#             # return redirect('contact/create-profile/')

#         return render(request,'Contact/create-profile.html', {
#             'form': submitted_form
#         })



# files

class CreateProfileView(FormView):
    template_name = 'Contact/create-profile.html'
    model = UserProfile
    form_class = ProfileForm
    fields = 'all'
    success_url = '/contact/create-profile'




class ListProfileView(ListView):
     template_name = 'Contact/profiles.html'
     model = UserProfile
     context_object_name = 'profiles'

    





    

     # def get(self, request):
     #        contact_form = ContactUsModelForm()
     #        return render(request,  'Contact/contact-us.html', {'contact_form':contact_form}  )

     # def post(self, request):
     #    contact_form = ContactUsModelForm(request.POST)
     #    if contact_form.is_valid():

     #       contact_form.save()
     #       return redirect('Home')
     #    return render(request,  'Contact/contact-us.html', {'contact_form':contact_form}  )



# def contact_page(request):
#     if request.method == 'POST':
#         # contact_form = ContactPageForm(request.POST)
#         contact_form = ContactUsModelForm(request.POST)


#         if contact_form.is_valid():
#            print(contact_form.cleaned_data)
#            contact = ContactUs(
#                title = contact_form.cleaned_data.get('title'),
#                Name_and_Surname = contact_form.cleaned_data.get('Name_and_Surname'),
#                Email = contact_form.cleaned_data.get('Email'),
#                Message = contact_form.cleaned_data.get('Message'),
#            )
#            contact.save()
#            return redirect('Home')
    
#     else:
#         contact_form = ContactUsModelForm()

#     return render(request, 'Contact/contact-us.html', {'contact_form':contact_form}  )



