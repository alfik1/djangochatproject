
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import FormView, CreateView, TemplateView, View 
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
# Create your views here.

#view for registration
class SignupView(CreateView):
    model = UserProfile
    form_class = RegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("signin")
    
    
class Signinview(FormView):
    template_name = "login.html"
    form_class = LoginForm
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pswd = form.cleaned_data.get("password")
            usr=authenticate(request, username = uname, password = pswd )
            if usr:
                login(request, usr)
                print(usr, "logged in")
                return redirect("home")
            else:
                print(usr, "not looged in")
                return render(request, self.template_name,{'form': form})
        
def signout_view(request, *args, **kwargs):
    
    logout(request)
    print("signout successfully")
    return redirect("signin")


class HomePageView(TemplateView):
    template_name = "base.html"


# To list the users in chat 
class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['user'] = UserProfile.objects.all()

        return context
    

class ChatDetailView(TemplateView):
    template_name = 'chat-detail.html'

    def get_context_data(self,   **kwargs):
        context = super().get_context_data(**kwargs)
        sender = DirectMessage.objects.filter(sender=self.request.user)
        context['sender'] = sender
        print(sender, "=====================================")
        
        recipient = self.kwargs['recipient_id']  # Assuming you have a recipient_id URL parameter
        recipient_messages = DirectMessage.objects.filter(recipient_id=recipient)
        context['recipient'] = recipient_messages
        print(recipient,"++++++++++++++++++++++++++++++")
        print(recipient_messages,"/**********")

        return context

    # def post(self, request, *args, **kwargs):
        
    #     form = MessageForm(request.POST)
    #     print(form.is_valid(),'?????????????????????????????????????????????????????????????')
    #     if form.is_valid():
    #         sender_id = request.user.id
    #         recipient_id = kwargs['recipient_id']
    #         message = form.cleaned_data['message']

    #         # Create a new DirectMessage object
    #         direct_message = DirectMessage.objects.create(
    #             sender_id=sender_id,
    #             recipient_id=recipient_id,
    #             message=message
    #         )
    #         return redirect('chat-detail', id=recipient_id)
    #     else:
    #         print(kwargs,'///////////////////////////////////////////////////')
    #         context = self.get_context_data(**kwargs)
    #         context['form'] = form
    #         return self.render_to_response(context)
    


