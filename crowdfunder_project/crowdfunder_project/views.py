from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods
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

@login_required
def new_project(request):
    form = ProjectForm()
    context = {'form': form}
    return render(request, 'create_project.html', context)

@login_required
def add_reward(request, id):
    form = RewardForm()
    # [print(data) for data in form]
    context = {'form': form, 'pid': id}
    return render(request, 'add_reward.html', context)

@login_required
def save_reward(request, id):
    form = RewardForm(request.POST)

    # [print(data, ':', form.cleaned_data[data]) for data in form.cleaned_data]
    [print(data, ':', request.POST[data]) for data in request.POST]
    if form.is_valid():
        new_reward = Reward()
        project = Project.objects.get(id=id)
        print('project:',project, '--','id:',id)
        new_reward.project = project
        new_reward.name = form.cleaned_data['name']
        new_reward.message = form.cleaned_data['message']
        new_reward.pledge_for = form.cleaned_data['pledge_for']
        new_reward.save()
        return redirect(reverse('show_project', kwargs={'id':id}))
    else:
        context = {'error_msg': 'You have invalid form, try again!', 'form': form, 'pid': id}
        return render(request, 'add_reward.html', context)

@login_required
def donate_reward(request, id):
    a_donation = Donation()
    a_donation.amount = request.POST['amount']
    a_donation.ily_message = request.POST['ily_message']
    a_donation.donator = request.user
    reward_id = request.POST['reward']
    a_donation.reward = Reward.objects.get(id=reward_id)
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        a_donation.save()
        return render(request, 'project_details.html', {
            'project': project,
            'donate_msg': 'you have just donated here',
            'reward_id': reward_id
        })
    else:
        return render(request, 'project_details.html', {
            'project': project,
            'donate_msg': 'error while donating',
            'reward_id': reward_id
        })

@login_required
def save_comment(request, id):
    form = CommentForm(request.POST)

    if form.is_valid():
        a_comment = Comment()
        project = Project.objects.get(id=id)
        a_comment.project = project
        a_comment.title = form.cleaned_data['title']
        a_comment.message = form.cleaned_data['message']
        a_comment.user = request.user
        a_comment.save()
        return redirect(reverse('show_project', kwargs={'id':id}))
    else:
        context = {'error_msg': 'You have invalid form, try again!', 'form': form, 'pid': id}
        return render(request, reverse('show_project', kwargs={'id':id}) , context)

@login_required
def create_project(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        # [print(data, '', form.cleaned_data[data]) for data in form.cleaned_data]
        new_project = Project()
        new_project.owner = request.user
        new_project.category = form.cleaned_data['category']
        new_project.title = form.cleaned_data['title']
        new_project.description = form.cleaned_data['description']
        new_project.budget = form.cleaned_data['budget']
        new_project.start_dtime = form.cleaned_data['start_dtime']
        new_project.end_dtime = form.cleaned_data['end_dtime']
        new_project.image = form.cleaned_data['image']
        new_project.save()
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

def show_project(request, id):
    project = Project.objects.get(id=id)
    comment_form = CommentForm()
    context = {'project': project, 'comment_form': comment_form, 'error_msg': 'You have invalid form, try again!'}
    return render(request, 'project_details.html', context)
    
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
        return HttpResponseRedirect('/home')
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

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')

@login_required
def my_profile(request):
    user_profile = request.user
    projects_own = user_profile.projects.all()
    projects_funded = set()
    donations = user_profile.charities.all()
    for donate in donations:
        projects_funded.add(donate.reward.project)
    total_amount_pledged = 0
    charities = user_profile.charities.all()
    for charity in charities:
        total_amount_pledged += int(charity.amount)
    context = {'projects_own': projects_own, 'projects_backed': projects_funded, 'pledged_amount': total_amount_pledged}
    return render(request, 'profile_page.html', context)


@login_required
def update_project(request, id):
    project = Project.objects.get(id=id)
    if request.user == project.owner: 
        print('error1111111111111')

        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect('show_project', id=project.id)
        else:
            form = ProjectForm(instance=project) 
        html_response = render(request, 'update_project.html', {'form': form, 'project': project})
        return HttpResponse(html_response)
    else:
        print('error')
        return HttpResponse("Error: <br>You don't have rights to update any changes.<br>You can only update the projects you own!")
