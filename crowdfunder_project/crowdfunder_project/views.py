from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from crowdfunder_project.forms import ProjectForm

def create_project(request):
    form = ProjectForm(request.POST)
    new_project = form.instance
    # reservation.user = request.user
    if form.is_valid():
        form.save()
        return redirect(reverse('project_show', args=[restaurant.pk]))
    else:
        context = {'restaurant': restaurant, 'reservation_form': form, 'title': restaurant.name}
        return render(request, 'restaurant_details.html', context)
