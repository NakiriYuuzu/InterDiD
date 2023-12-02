from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from InterDiD import settings
from ServerApi.serializer import ArtworksSerializer
from ServerCommon.models import Artworks
import random


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
    artwork = Artworks.objects.all()
    serializer = ArtworksSerializer(artwork, many=True)
    result = serializer.data
    data = {
        'title': settings.APP_NAME,
        'image': settings.APP_HOST + result[0]['artwork_items'][0]['artwork_item_image'],
        'url': settings.APP_HOST,
    }
    return render(request, 'index.html', locals())


def puzzle(request):
    artwork = Artworks.objects.all()
    serializer = ArtworksSerializer(artwork, many=True)
    result = serializer.data
    data = {
        'title': settings.APP_NAME,
        'image': settings.APP_HOST + random_image(result),
        'url': settings.APP_HOST,
    }
    return render(request, 'puzzle.html', locals())


def artworks(request):
    artwork_id = request.GET.get('id', None)
    if artwork_id:
        artwork = Artworks.objects.filter(artwork_id=artwork_id)
        serializer = ArtworksSerializer(artwork, many=True)
        result = serializer.data
        data = {
            'title': result[0]['product_title'],
            'image': settings.APP_HOST + result[0]['artwork_items'][0]['artwork_item_image'],
            'url': settings.APP_HOST + '/artworks?id=' + artwork_id,
        }
    else:
        data = {
            'url': settings.APP_HOST + '/artworks',
        }
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


def random_image(artwork_list):
    # random_artworks = random.choice(artwork_list)
    random_artworks = artwork_list[0]
    random_artwork_items = random.choice(random_artworks['artwork_items'])
    random_artwork_image = random_artwork_items['artwork_item_image']
    return random_artwork_image
