# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.utils import timezone

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # already logged in

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                if not request.POST.get('remember_me'):
                    request.session.set_expiry(0)  # expires on browser close
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('/')
            else:   
                messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/accounts/login')