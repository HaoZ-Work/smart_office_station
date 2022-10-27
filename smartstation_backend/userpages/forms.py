import imp
from inspect import ArgSpec
from tkinter import HIDDEN
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm


# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)


class LoginForm(AuthenticationForm):
	# def __init__(self, request, *args, **kwargs):
	# 	super().__init__(request, *args, **kwargs)
	# 	self.dev= kwargs
	DevId = forms.IntegerField(label='Device ID',required=True)
	
	

	# def getDevId(self):
	# 	return self.kwargs
	# DevId = forms.IntegerField(label='Device ID',required=False,initial=super().kwargs)

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
                    user.save()
                    send_mail('Sign up successfully!', 'Your account is available now!', 'dtdysh@gmail.com', [user.email])



		return user