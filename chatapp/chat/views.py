
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .models import *
from django.views.generic import FormView, CreateView, TemplateView, View 
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
import pusher
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileUploadSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

#create your views

def send_pusher_event(channel, event, data):
    pusher_client = pusher.Pusher(
        app_id='1612620',
        key='99d02ed61a52d34cd27c',
        secret='a771625449c032e69817',
        cluster='mt1',
        ssl=True
    )
    pusher_client.trigger(channel, event, data)


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
        query = Q(sender_id__in=[request.user.id, id]) & Q(recipient_id__in=[request.user.id, id])
        msgs = DirectMessage.objects.filter(query).order_by('timestamp')
        form = MessageForm()

        # Update the DirectMessage objects with the file_url field
        for message in msgs:
            print(message.file_url,"*--*-**-*-*--*-*-*-*-*-*--*--*-*")

        context = {
            'messages': msgs,
            'form': form,
            'recipient_id': recipient_id,
            'allowed_extensions': ['.jpg', '.jpeg', '.png', '.gif'],
            'video_extensions': ['.mp4', '.avi', '.mov'],
  
        }
        print(context,"/////////////////")
        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            rec_id = id
            message = form.cleaned_data.get("message")
            sender = request.user
            recipient = get_object_or_404(User, id=rec_id)
            direct_message = DirectMessage.objects.create(sender=sender, recipient=recipient, message=message)

            # Use the existing pusher_client instance to trigger the event
            send_pusher_event('my-channel', 'my-event', {
                'message': direct_message.message,
                'sender': direct_message.sender.username,
                'recipient': direct_message.recipient.username,
                'file': request.POST.get('file'),  # Pass the file_url from the form data
            })

            return redirect('chat-detail', id=rec_id)
        else:
            # Handle form errors if needed
            pass

    
        
class FileUploadView(APIView):
    def post(self, request, id, format=None):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            recp_id = id
            sender = request.user
            recipient = get_object_or_404(User, id=recp_id)

            file = serializer.validated_data.get('file')  # Get the uploaded file

            # Save the file to your file storage system
            file_path = default_storage.save(f'media/{file.name}', ContentFile(file.read()))

            # Generate the URL for the file
            file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
            print(file_url, "****************************************")

            # Save the file and the file URL to the database
            message = serializer.save(sender=sender, recipient=recipient, file=file_path, file_url=file_url)
            message_data = {
                'sender': message.sender.username,
                'file_url': message.file_url,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            # pusher  event trigger
            send_pusher_event('my-channel', 'my-event', message_data)
            
            return JsonResponse(message_data)

        return Response(serializer.errors, status=400)