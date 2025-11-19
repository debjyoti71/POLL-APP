from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            request.session['user_id'] = user.id
            request.session.save()  # Explicitly save session
            print(f"DEBUG: User {user.username} registered, session user_id: {request.session.get('user_id')}")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session.save()  # Explicitly save session
                    print(f"DEBUG: User {user.username} logged in, session user_id: {request.session.get('user_id')}")
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')