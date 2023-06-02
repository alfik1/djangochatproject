
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import FormView, CreateView, TemplateView, View 
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.db.models import Q
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
    
    # def get_context_data(self, **kwargs):
        
    #     context = super().get_context_data(**kwargs)
    #     sender = DirectMessage.objects.filter(sender=self.request.user)
        
    #     context['sender'] = sender
    #     print(sender, "======This is  Sender Message =====")
        
    #     recipient_id = kwargs['recipient_id'] 
    #     print("*********" , recipient_id)
    #     query = (
    #             Q(sender=sender, recipient_id=recipient_id) |
    #             Q(sender_id=recipient_id, recipient=sender)
    #         )
    #     recipient_messages = DirectMessage.objects.filter(query)
    #     context['recipient'] = recipient_messages
    #     print(recipient_messages,"*******This is recipient message ******")
    #     return context
    
     # def get(self, request, *args, **kwargs):
    #     sender_id = request.GET.get('sender_id')
    #     recipient_id = request.GET.get('recipient_id')
    #     print(sender_id, "******************")
    #     print(recipient_id, "********************")
    #     query = Q(Q(sender_id=sender_id) & Q(recipient_id=recipient_id)) | Q(Q(sender_id=recipient_id) & Q(recipient_id=sender_id))
    #     msgs = DirectMessage.objects.filter(query).order_by('timestamp')
    #     form = MessageForm()
    #     context = {
    #         'messages': msgs,
    #         'form': form,
    #     }
    #     return render(request, self.template_name, context)
    
    
    # def post(self, request, *args, **kwargs):
    #     form = MessageForm(request.POST)
    #     if form.is_valid():
    #         sender_id = request.POST.get('sender_id', '')
    #         recipient_id = request.POST.get('recipient_id', '')
    #         msg = form.cleaned_data['message']

    #         sender_user = User.objects.get(pk=sender_id)
    #         receiver_user = User.objects.get(pk=recipient_id)

    #         try:
    #             msg_obj = DirectMessage.objects.create(sender=sender_user, receiver=receiver_user, message=msg)
    #             return self.render_to_response(self.get_context_data())
    #         except:
    #             form.add_error(None, 'Error occurred while saving the message.')

    #     return self.render_to_response(self.get_context_data(form=form))
    
    


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



    def get(self, request, id, *args, **kwargs):
        sender_id = request.user.id
        recipient_id = id
        print(sender_id, "******************")
        print(recipient_id, "******************")
        query = Q(Q(sender_id=self.request.user) & Q(recipient_id=id)) | Q(Q(sender_id=id) & Q(recipient_id=self.request.user))
        print(query,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        msgs = DirectMessage.objects.filter(query).order_by('timestamp')
        print(msgs)
        form = MessageForm()
        context = {
            'messages': msgs,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            sender_id = request.POST.get('sender_id', '')
            recipient_id = request.POST.get('recipient_id', '')
            msg = form.cleaned_data['message']

            sender_user = User.objects.get(pk=sender_id)
            receiver_user = User.objects.get(pk=recipient_id)

            try:
                msg_obj = DirectMessage.objects.create(sender=sender_user, receiver=receiver_user, message=msg)
                return self.render_to_response(self.get_context_data())
            except:
                form.add_error(None, 'Error occurred while saving the message.')

        return self.render(self.template_name(form=form))

    
    

   