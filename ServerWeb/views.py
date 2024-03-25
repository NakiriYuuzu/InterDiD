from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from InterDiD import settings
from ServerApi.serializer import ArtworksSerializer
from ServerCommon.models import Artworks, Games
import random


def sign_in(request):
    next_url = request.GET.get('next', '/admin')
    if request.method == 'POST':
        acc = request.POST.get('account')
        pwd = request.POST.get('password')
        print(acc, pwd)
        user = authenticate(request, username=acc, password=pwd)

        if user is not None:
            login(request, user)
            if not user.is_superuser:
                next_url = '/admin/list_artwork'
            return JsonResponse({'success': True, 'next_url': next_url})
        else:
            return JsonResponse({'success': False, 'error': 'Wrong account or password'})
    else:
        return render(request, 'auth/sign-in.html', locals())


def index(request):
    artwork = Artworks.objects.all()
    serializer = ArtworksSerializer(artwork, many=True)
    result = serializer.data
    if result:
        image = random_image(result)
    else:
        image = '/static/images/pages/01-page.png'
    data = {
        'title': settings.APP_NAME,
        'image': settings.APP_HOST + image,
        'url': settings.APP_HOST,
    }
    return render(request, 'index.html', locals())


def puzzle(request):
    global game
    try:
        image = random_image(ArtworksSerializer(Artworks.objects.all(), many=True).data)
        print(image)
        game = Games.objects.filter(game_diff_select=1)
        error = ''
    except Exception as e:
        image = ''
        error = str(e)

    if game[0] is None:
        error = 'No game data'

    data = {
        'title': settings.APP_NAME,
        'image': settings.APP_HOST + image,
        'url': settings.APP_HOST,
        'error': error,
        'game_id': game[0].game_id if game else None,
        'diff': game[0].game_diff if game else 0,
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
        'title': settings.APP_NAME,
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'dashboard/dashboard.html', msg)


@login_required
def accounts(request):
    msg = {
        'title': settings.APP_NAME,
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'dashboard/accounts.html', msg)


@login_required
def games(request):
    msg = {
        'title': settings.APP_NAME,
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'dashboard/games.html', msg)


@login_required
def form_beacon(request):
    msg = {
        'title': settings.APP_NAME,
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'dashboard/form_beacon.html', msg)


@login_required
def list_artwork(request):
    msg = {
        'title': settings.APP_NAME,
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'dashboard/list_artwork.html', msg)


@login_required
def form_artwork(request):
    msg = {
        'title': settings.APP_NAME,
        'mode': settings.DEBUG,
        'username': request.user.username[0].upper() + request.user.username[1:],
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'dashboard/form_artwork.html', msg)


@login_required
def sign_out(request):
    logout(request)
    return redirect('/admin/login/')


def random_image(artwork_list):
    try:
        ran = random.randint(0, len(artwork_list) - 1)
        random_artworks = artwork_list[ran]
        random_artwork_items = random.choice(random_artworks['artwork_items'])
        random_artwork_image = random_artwork_items['artwork_item_image']
        return random_artwork_image
    except Exception as e:
        return '0|' + e.__str__()
