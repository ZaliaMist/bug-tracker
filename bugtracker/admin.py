from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bugtracker.models import MyUser, TicketM
 
class BugtrackerAdmin(UserAdmin):
   fieldsets = UserAdmin.fieldsets + (
       (None, {"fields": ("display_name",)}),
   )
 
admin.site.register(MyUser, BugtrackerAdmin)
admin.site.register(TicketM)



