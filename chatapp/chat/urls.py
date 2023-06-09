from django.contrib import admin
from django.urls import path , include
from chat import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

    path('',views.HomePageView.as_view(), name='home'),
    path('signup/',views.SignupView.as_view(), name= 'signup'),
    path('login',views.Signinview.as_view(), name= 'signin'),
    path("signout/",views.signout_view, name="signout"),
    path("chat/",views.ChatView.as_view(), name="chat"),
    path("details/<int:id>",views.ChatDetailView.as_view(), name="chat-detail"),
    path('chat/<int:id>/', views.ChatDetailView.as_view(), name='send_message'),
    path('upload/<int:id>/', views.FileUploadView.as_view(), name='file-upload')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
