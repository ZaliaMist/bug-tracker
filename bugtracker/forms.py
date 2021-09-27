from django import forms
from bugtracker.models import MyUser
from django.utils import timezone
 
 
# logged in
class MyUserF(forms.Form):
   display_name = forms.CharField(max_length=100)


# signup
class AddUserForm(forms.Form):
   display_name = forms.CharField(max_length=100, required=False)
   username = forms.CharField(max_length=150)
   password = forms.CharField(widget=forms.PasswordInput)
 
 
# login to your acct page:
class LoginForm(forms.Form):
   username = forms.CharField(max_length=150)
   password = forms.CharField(widget=forms.PasswordInput)


class TicketF(forms.Form):
   title = forms.CharField(max_length=100)
   description = forms.CharField(widget=forms.Textarea)


class EditTicketF(forms.Form):
   title = forms.CharField(max_length=100)
   description = forms.CharField(widget=forms.Textarea)


