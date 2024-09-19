from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

@superuser_required
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} has been created successfully.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})

@superuser_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'profiles/user_list.html', {'users': users})

@superuser_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'profiles/edit_user.html', {'form': form, 'user': user})

@superuser_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return redirect('user_list')
    return render(request, 'profiles/delete_user.html', {'user': user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_home')  # Redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'profiles/login.html')