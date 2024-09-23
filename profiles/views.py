from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from index.models import Home

def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


def logout_view(request):
    logout(request)
    return redirect('/')


@superuser_required
def register_user(request):
    home = Home.objects.filter(is_active=True).first()
     
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} has been created successfully.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
        
    context = {
        'home': home,
        'form': form,
    }
    return render(request, 'profiles/register.html', context)

@superuser_required
def user_list(request):
    home = Home.objects.filter(is_active=True).first()
    users = User.objects.all()
    
    context = {
        'home': home,
        'users': users,
    }
    
    return render(request, 'profiles/user_list.html', context)

@superuser_required
def edit_user(request, user_id):
    home = Home.objects.filter(is_active=True).first()
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
        
    context = {
        'form': form,
        'user': user,
        'home': home,
    }    
    return render(request, 'profiles/edit_user.html', context)

@superuser_required
def delete_user(request, user_id):
    home = Home.objects.filter(is_active=True).first()
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return redirect('user_list')
    
    context = {
        'user': user,
        'home': home,
    }
    return render(request, 'profiles/delete_user.html', context)

def login_view(request):
    home = Home.objects.filter(is_active=True).first()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_home')  # Redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')
            
    context = {
        'home': home,
    }
    return render(request, 'profiles/login.html', context)