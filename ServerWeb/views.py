from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from InterDiD import settings


def sign_in(request):
    next_url = request.GET.get('next', '/admin')
    if request.method == 'POST':
        acc = request.POST['account']
        pwd = request.POST['password']
        user = authenticate(request, username=acc, password=pwd)

        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/admin')
        else:
            return render(request, 'auth/sign-in.html', {'error': 'Wrong account or password'})
    else:
        return render(request, 'auth/sign-in.html', locals())


def index(request):
    return render(request, 'index.html', locals())


def artworks(request):
    return render(request, 'artworks.html', locals())


@login_required
def dashboard(request):
    msg = {
        'title': 'InterDiD',
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
    }
    return render(request, 'dashboard/dashboard.html', msg)


@login_required
def games(request):
    msg = {
        'title': 'InterDiD',
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
    }
    return render(request, '404.html', msg)


@login_required
def form_beacon(request):
    msg = {
        'title': 'InterDiD',
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
    }
    return render(request, 'dashboard/form_beacon.html', msg)


@login_required
def list_artwork(request):
    msg = {
        'title': 'InterDiD',
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
    }
    return render(request, 'dashboard/list_artwork.html', msg)


@login_required
def form_artwork(request):
    msg = {
        'title': 'InterDiD',
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
    }
    return render(request, 'dashboard/form_artwork.html', msg)


@login_required
def sign_out(request):
    logout(request)
    return redirect('/admin/login/')
