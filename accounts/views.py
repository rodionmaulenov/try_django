from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/admin')
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    return render(request, 'accounts/logout.html')
