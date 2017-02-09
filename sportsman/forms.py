from django import forms
import datetime
from .models import Participant, TeamManager
from django.contrib.auth.models import User
from django.forms.extras import SelectDateWidget


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control', 'name': 'password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control', 'name': 'username'}))

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email ID', 'required': 'required', 'class': 'form-control'}))


    mobile_phone = forms.CharField(
            widget=forms.NumberInput(attrs={'placeholder': 'Mobile Number',  'required': 'required', 'class': 'form-control'}))
    team_name = forms.CharField(label='Team Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Team Name',
                                                              'required': 'required', 'class': 'form-control',}))

    password1 = forms.CharField(label='Password', max_length='12',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'required': 'required', 'class': 'form-control',}))
    password2 = forms.CharField(label='Confirm Password', max_length='12',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'required': 'required',
                                                                  'oninput': 'check(this)', 'class': 'form-control',}))
    address = forms.CharField(label='Address',
                                widget=forms.TextInput(attrs={'placeholder': 'Address',
                                                              'required': 'required', 'class': 'form-control',}))
    manager_name = forms.CharField(label='Manager Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Manager Name',
                                                              'required': 'required', 'class': 'form-control',}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
        return email

class ParticipantForm(forms.ModelForm):
    date_of_birth=forms.DateField(widget=SelectDateWidget(years=range(1980, 2012)))
    first_name = forms.CharField(label='First Name',
                                widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                              'required': 'required', 'class': 'form-control',}))
    middle_name = forms.CharField(label='Middle Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'Middle Name',
                                                               'required': 'required', 'class': 'form-control', }))
    last_name = forms.CharField(label='Last Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                               'required': 'required', 'class': 'form-control', }))

    class Meta:
        error_css_class = 'error'
        model = Participant
        exclude = ['team_manager', 'age', 'is_approved']

class PasswordUpdateForm(forms.Form):
    password1 = forms.CharField(label='Password', max_length='12',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'required': 'required', 'class': 'form-control', }))
    password2 = forms.CharField(label='Confirm Password', max_length='12',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'required': 'required',
                                                                  'oninput': 'check(this)', 'class': 'form-control', }))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

class EditProfileForm(forms.ModelForm):

    mobile_phone = forms.CharField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'Mobile Number', 'required': 'required', 'class': 'form-control'}))
    team_name = forms.CharField(label='Team Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Team Name',
                                                              'required': 'required', 'class': 'form-control', }))
    address = forms.CharField(label='Address',
                              widget=forms.TextInput(attrs={'placeholder': 'Address',
                                                            'required': 'required', 'class': 'form-control', }))
    manager_name = forms.CharField(label='Manager Name',
                                   widget=forms.TextInput(attrs={'placeholder': 'Manager Name',
                                                                 'required': 'required', 'class': 'form-control', }))
    class Meta:
        model = TeamManager
        exclude =['user']



