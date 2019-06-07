from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from crowdfunder_project.forms import ProjectForm, LoginForm
from django.forms import ModelForm
from crowdfunder_project.models import *
from crowdfunder_project.forms import *

def root(request):
    return HttpResponseRedirect('/home')

def home_page(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'home.html', context)

def new_project(request):
    form = ProjectForm()
    context = {'form': form}
    return render(request, 'create_project.html', context)

def create_project(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home_page')
    else:
        context = {'error_msg': 'You have invalid form, try again!', 'form': form}
        response = render(request, 'create_project.html', context)
        return HttpResponse(response)

def search_project(request):
    query = request.GET['query']
    search_results = Project.objects.filter(title=query)
    context = {'projects': search_results, 'query': query}
    response = render(request, 'search.html', context)
    return HttpResponse(response)

        
# def show_project(request, project_id):
    # show_project = Project.objects.get(id=project_id)
    # context = {'form': form, 'error_msg': 'You have invalid form, try again!'}
    # return render(request, 'new_project.html', context)

# @login_required
# def backer_page(request):
#     if request.method == 'POST':
#         form = BackerForm(request.POST)
#         if form.is_valid():
#             backproject = from.save(commit=False)
#             backproject.user = request.user
#             form.save()
#             return
#         else:


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('home_page')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()
    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
