from django.contrib import admin
from django.urls import path , include
from chat import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

    path('',views.HomePageView.as_view(), name='home'),
    path('signup/',views.SignupView.as_view(),name= 'signup'),
    path('login',views.Signinview.as_view(),name= 'signin'),
    path("signout/",views.signout_view,name="signout"),
    path("chat/",views.ChatView.as_view(),name="chat"),
    # path('chat-detail/<int:sender_id>/<int:recipient_id>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path("details/<int:id>",views.ChatDetailView.as_view(),name="chat-detail"),
    # path('send-message/<int:recipient_id>/', views.ChatDetailView.as_view(), name='send_message'),
    

        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
