from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from InterDiD import settings


def sign_in(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        acc = request.POST['account']
        pwd = request.POST['password']
        user = authenticate(request, username=acc, password=pwd)

        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/')
        else:
            return render(request, 'auth/sign-in.html', {'error': 'Wrong account or password'})
    else:
        return render(request, 'auth/sign-in.html', locals())


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    # User Name
    username = request.user.username[0].upper() + request.user.username[1:]

    return render(request, 'index.html', locals())


@login_required
def form_artwork(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    # User Name
    username = request.user.username[0].upper() + request.user.username[1:]

    return render(request, 'form/form_artwork.html', locals())


@login_required
def sign_out(request):
    logout(request)
    return redirect('/')
