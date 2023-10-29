from django.contrib import admin
from .models import *


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("id","title","token","is_active")
    list_display_links = ("id","title")  
    save_as = True 

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id","name","chat_id", "token","is_active")
    list_display_links = ("id","name") 
    save_as = True 

# admin.site.register(Chat)

admin.site.site_title = "TeleBot 0.1v"
admin.site.site_header = "TeleBot 0.1v"