from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^participant/(?P<pk>\d+)/edit/$', views.paticipant_edit, name='participant_edit'),
    url(r'^participant/new/$', views.participant_new, name='participant_new'),
    url(r'^search/$', views.searchResults, name='searchResults'),
    url(r'^participant/(?P<pk>\d+)/delete/$', views.paticipant_delete, name='participant_delete'),
    url(r'^participant/approved/$', views.participant_approved, name='participant_approved'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
]