from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from crowdfunder_project.forms import ProjectForm
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
        
# def show_project(request, project_id):
    # show_project = Project.objects.get(id=project_id)
    # context = {'form': form, 'error_msg': 'You have invalid form, try again!'}
    # return render(request, 'new_project.html', context)


