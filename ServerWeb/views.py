from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect

from InterDiD import settings
from ServerCommon.models import Artworks, Beacons


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
@transaction.atomic
def form_beacon(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    # Init Data
    username = request.user.username[0].upper() + request.user.username[1:]
    beacon_list = Beacons.objects.all()
    artwork_list = Artworks.objects.all()
    print(len(beacon_list))

    if request.method == 'POST':
        action = request.POST.get('action', None)
        artwork = request.POST.get('artwork', None)
        beacon_name = request.POST.get('ble_name', None)
        beacon_uuid = request.POST.get('ble_uuid', None)

        if not (beacon_name and beacon_uuid):
            messages.error(request, 'Please fill beacon name and uuid!')
            return redirect('/form_beacon/')

        if len(beacon_list) >= 10:
            messages.error(request, 'Please fill beacon less than 10!')
            return redirect('/form_beacon/')

        if len(beacon_uuid) >= 10:
            messages.error(request, 'Please fill uuid less than 10 characters!')
            return redirect('/form_beacon/')

        try:
            if action == 'add':
                Beacons.objects.create(
                    beacon_name=beacon_name,
                    beacon_uuid=beacon_uuid,
                    artworks_id=artwork,
                )
                messages.success(request, f'successfully add {beacon_name}.')
                return redirect('/form_beacon/')
            elif action == 'edit':
                beacon, created = Beacons.objects.update_or_create(
                    beacon_uuid=beacon_uuid,
                    defaults={'beacon_name': beacon_name, 'artworks_id': artwork}
                )
                messages.success(request, f'successfully edit {beacon_name}.')
                return redirect('/form_beacon/')
        except IntegrityError:
            return redirect('/form_beacon/')

    return render(request, 'form/form_beacon.html', locals())


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
