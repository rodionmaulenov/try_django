from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def login_view(request):
    context = {}

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if not user:
            context['error'] = 'Not valid username or password'
            return render(request, 'accounts/login.html', context)
        login(request, user)
        return redirect('/admin')
    return render(request, 'accounts/login.html', {})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    return render(request, 'accounts/logout.html')