from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator, RegexValidator
from django import forms
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.messages.views import SuccessMessageMixin

class TeamManager(models.Model):
    user = models.ForeignKey('auth.User')
    team_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    manager_name = models.CharField(max_length =30)
    mobile_phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])

    def __str__(self):
        return self.team_name

class Participant(models.Model):
    SWIMMING_EVENT_CHOICES = (
        ('50m Freestyle', '50m Freestyle'),
        ('100m Freestyle','100m Freestyle'),
        ('200m Freestyle', '200m Freestyle'),
        ('50m Butterfly', '50m Butterfly'),
        ('100m Butterfly', '100m Butterfly'),
        ('200m Butterfly', '200m Butterfly'),
        ('50m Brest Stroke', '50m Brest Stroke'),
        ('100m Brest Stroke', '100m Brest Stroke'),
        ('200m Brest Stroke', '200m Brest Stroke'),
        ('50m Back Stroke', '50m Back Stroke'),
        ('100m Back Stroke', '100m Back Stroke'),
        ('200m Back Stroke', '200m Back Stroke'),
        ('Individual Medley 100m', 'Individual Medley 100m'),
        ('Individual Medley 200m', 'Individual Medley 200m'),
    )
    GENDER_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    team_manager = models.ForeignKey(TeamManager, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    birth_certificate = models.ImageField(upload_to='images', default='images/not_available.jpg')
    gender = models.CharField(max_length=6, choices=GENDER_OPTIONS)
    events_list = MultiSelectField(choices=SWIMMING_EVENT_CHOICES, max_choices=4)
    age = models.IntegerField()
    is_approved = models.BooleanField()

    def __str__(self):
        return self.first_name
