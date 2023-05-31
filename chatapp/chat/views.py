
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
    model = UserProfile
    template_name = 'chat-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = UserProfile.objects.get(id =kwargs['id'])
        return context



    
class SendMessageView(View):
    def get(self, request, recipient_id):
        form = MessageForm()
        recipient = User.objects.get(id=recipient_id)
        messages = DirectMessage.objects.filter(sender=request.user, recipient=recipient) | DirectMessage.objects.filter(sender=recipient, recipient=request.user)
        messages = messages.order_by('timestamp')
        context = {'form': form, 'user_id': recipient, 'messages': messages}
        return render(request, 'chat-detail.html', context)

    def post(self, request, recipient_id):
        form = MessageForm(request.POST)
        recipient = User.objects.get(id=recipient_id)
        if form.is_valid():
            message = form.cleaned_data['message']
            DirectMessage.objects.create(sender=request.user, recipient=recipient, message=message)
            
        return redirect('send_message', recipient_id=recipient_id)