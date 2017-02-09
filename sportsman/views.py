from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .forms import LoginForm, RegisterForm, ParticipantForm, PasswordUpdateForm, EditProfileForm
from .models import TeamManager, Participant
from django.contrib.auth.models import User
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import views

@login_required(login_url='/login/')
def index(request):
    me = TeamManager.objects.get(user=request.user)
    participant_list = Participant.objects.filter(team_manager=me)
    if participant_list.exists():
        page = request.GET.get('page', 1)
        paginator = Paginator(participant_list, 4)
        try:
            participant_list = paginator.page(page)
        except PageNotAnInteger:
            participant_list = paginator.page(1)
        except EmptyPage:
            participant_list = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'participant_list': participant_list})

def login_user(request):
    if request.user.is_authenticated():
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                print("Login Success")
                login(request, user)
                return redirect('index')
            else:
                print("Login Failed")
                messages.add_message(request, messages.ERROR, 'Login failed. Please try again')
                return render(request, "login.html", {'form': form, 'user':user})

        else:
            return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    return render(request, "login.html", {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            if user is not None:
                TeamManager.objects.create(user=user,
                                           team_name=form.cleaned_data['team_name'],
                                           address=form.cleaned_data['address'],
                                           manager_name=form.cleaned_data['manager_name'],
                                           mobile_phone=form.cleaned_data['mobile_phone']
                                           )
                messages.add_message(request, messages.SUCCESS, 'Successfully created user. Please login to continue...')
                return redirect('login')
            else:
                messages.add_message(request, messages.ERROR, 'User creation failed. Please try again')
                return render(request, "register.html", {'form': form})
        else:
            return render(request, "register.html", {'form': form})
    else:
        return render(request, "register.html", {'form': RegisterForm()})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def paticipant_edit(request, pk):
    me = TeamManager.objects.get(user=request.user)
    try:
        instance = get_object_or_404(Participant, pk=pk, team_manager=me, is_approved=False)
    except:
        raise Http404("No Participant matches the given query.")
    print instance
    if request.method == "POST":
        form = ParticipantForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.team_manager = me
            participant.is_approved = False
            participant.age = calculate_age(form.cleaned_data['date_of_birth'])
            participant.birth_certificate = form.cleaned_data['birth_certificate']
            participant.save()
            participant_list = Participant.objects.filter(team_manager=me)
            messages.add_message(request, messages.SUCCESS, 'Successfully edited participant information.')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Editing participant information failed. Please try again')
    else:
        form = ParticipantForm(instance=instance)
    return render(request, 'edit_participant.html', {'form': form})

@login_required(login_url='/login/')
def participant_new(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            me = TeamManager.objects.get(user=request.user)
            participant.team_manager = me
            participant.age = calculate_age(form.cleaned_data['date_of_birth'])
            participant.is_approved = False
            participant.birth_certificate = form.cleaned_data['birth_certificate']
            participant.save()
            participant_list = Participant.objects.filter(team_manager=me)
            messages.add_message(request, messages.SUCCESS, 'Successfully added participant information.')
            return redirect('index')
    else:
        form = ParticipantForm()
    return render(request, 'edit_participant.html', {'form': form})

@login_required(login_url='/login/')
def searchResults(request):
    q = request.GET.get("q")
    me = TeamManager.objects.get(user=request.user)
    results = Participant.objects.filter(first_name__contains=q,team_manager=me)
    return render(request, "index.html", {'participant_list': results})

@login_required(login_url='/login/')
def paticipant_delete(request, pk):
    me = TeamManager.objects.get(user=request.user)
    participant = Participant.objects.filter(pk=pk, team_manager=me)
    participant.delete()
    messages.add_message(request, messages.SUCCESS, 'Successfully deleted participant information.')
    return redirect('index')

@login_required(login_url='/login/')
def participant_approved(request):
    me = TeamManager.objects.get(user=request.user)
    participant_list = Participant.objects.filter(team_manager=me, is_approved=True)
    if participant_list.exists():
        page = request.GET.get('page', 1)
        paginator = Paginator(participant_list, 4)
        try:
            participant_list = paginator.page(page)
        except PageNotAnInteger:
            participant_list = paginator.page(1)
        except EmptyPage:
            participant_list = paginator.page(paginator.num_pages)
    return render(request, 'approved_participants.html', {'participant_list': participant_list})

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            u = request.user
            u.set_password(password1)
            u.save()
            if u is not None:
                messages.add_message(request, messages.SUCCESS, 'Successfully changed password')
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Password change failed. Please try again')
                return render(request, "change_password", {'form': form})
        else:
            return render(request, "change_password.html", {'form': form})
    else:
        return render(request, "change_password.html", {'form': PasswordUpdateForm()})

@login_required(login_url='/login/')
def update_profile(request):
    me = TeamManager.objects.get(user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=me)
        if form.is_valid():
            team_manager = form.save(commit=False)
            team_manager.team_name = form.cleaned_data['team_name']
            team_manager.address = form.cleaned_data['address']
            team_manager.manager_name = form.cleaned_data['manager_name']
            team_manager.mobile_phone = form.cleaned_data['mobile_phone']
            team_manager.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully edited profile information.')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Editing profile information failed. Please try again')
    else:
        form = EditProfileForm(instance=me)
    return render(request, 'update_profile.html', {'form': form})

def calculate_age(born):
    today = date.today()
    print today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
