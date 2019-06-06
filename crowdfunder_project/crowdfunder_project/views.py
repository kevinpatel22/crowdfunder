from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from crowdfunder_project.forms import ProjectForm

def new_project(request):
    form = ProjectForm()
    # new_project = form.instance
    # reservation.user = request.user
    context = {'new_project': form}
    return render(request, 'new_project.html', context)
