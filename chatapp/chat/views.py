
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import FormView, CreateView, TemplateView, View 
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from pusher import Pusher

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
    

class ChatDetailView(View):
    
    template_name = 'chat-detail.html'

    
    def get(self, request, id):
        sender_id = request.user.id
        recipient_id = get_object_or_404(User, id=id)
        # print(sender_id, "******************")
        # print(recipient_id, "******************")
        query = Q(sender_id__in=[request.user.id, id]) & Q(recipient_id__in=[request.user.id, id])
        msgs = DirectMessage.objects.filter(query).order_by('timestamp')
        # print(msgs)
        form = MessageForm()
        context = {
            'messages': msgs,
            'form': form,
            'recipient_id':recipient_id
        }
        return render(request, self.template_name, context)
    

    
    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            rec_id = kwargs.get('id')  
            message = form.cleaned_data.get("message")
            user = self.request.user 
            recipient = User.objects.get(id=rec_id)
            message = form.cleaned_data['message']
            DirectMessage.objects.create(sender=user, recipient=recipient, message=message)

            # Trigger a Pusher event to notify other users about the new message
            pusher = Pusher(
                app_id=settings.PUSHER_APP_ID,
                key=settings.PUSHER_KEY,
                secret=settings.PUSHER_SECRET,
                cluster=settings.PUSHER_CLUSTER,
                ssl=True
            )
            pusher.trigger('chat-room', 'new-message', {
                'message': message,
                'sender': user.username,
            })

        return redirect('chat-detail', id=rec_id)

    

    
    

   