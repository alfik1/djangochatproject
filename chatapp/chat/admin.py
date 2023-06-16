from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(DirectMessage)
admin.site.register(Group)
admin.site.register(GroupChat)



