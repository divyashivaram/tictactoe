# from http.client import HTTPResponse
from .forms import NameForm
import json
from venv import create
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

# connect to Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


@api_view(['GET'])
def index(request, *args, **kwargs):
    return render(request, 'landing.html', {})


@api_view(['POST'])
def create_or_join_game(request, *args, **kwargs):
    form = NameForm(request.POST)
    player_name = form.data['your_name']

    last_game = get_last_game()

    if last_game is None or last_game['O'] is not None:
        game_id = create_new_game(player_name)
        # update_game_id_in_storage()
    else:
        game_id = redis_instance.get('GameId').decode("utf-8")
        add_second_player(player_name, game_id)

    # redirecting with a query param and an argument. Hence constructing the redirect url right away using 'format'
    return redirect('{}?player_name={}'.format(reverse('get_game', args=[game_id]), player_name))


def get_key(my_dict, val):
    """
    Get key from value in dict
    """
    for key, value in my_dict.items():
        if val == value:
            return key
    return None


@api_view(['GET'])
def render_game(request, *args, **kwargs):
    player_name = str(request.GET.get('player_name', None))
    game = get_game_object(kwargs['game_id'])
    context = {'game': game, 'player_sign': get_key(game, player_name)}
    print('CONTEXT: ', context)
    # TODO: Handle error here. Page does not exist, throw exception etc
    # example:
    # from django.http import Http404
    # try:
    #     board = board.objects.get(pk=game_id)
    # except board.DoesNotExist:
    #     raise Http404("Game does not exist")
    return render(request, 'board.html', context)


@api_view(['GET'])
def get_moves(request, game_id):
    # Fetch moves and return
    return JsonResponse({'gameId': game_id, 'moves': list(range(9))})


@api_view(['GET'])
def get_all_games(request, *args, **kwargs):
    games = json.loads(redis_instance.get('Games'))
    response = {
        'Games': games
    }
    return Response(response, status=200)


@api_view(['POST'])
def update_moves(request, *args, **kwargs):
    game_id = json.loads(request.body)['gameId']
    moves = json.loads(request.body)['moves']
    games = json.loads(redis_instance.get('Games'))
    game_object = games[game_id.decode("utf-8")]
    game_object['moves'] = moves
    # receive game id, player 'X' or 'O', then index
    # Get game object
    # Update moves list and update the game object in redis
    return


def add_second_player(player_name, game_id):
    games = json.loads(redis_instance.get('Games'))
    current_game = games[game_id]
    current_game['O'] = player_name
    redis_instance.set('Games', json.dumps(games))


def get_game_object(game_id):
    return json.loads(redis_instance.get('Games'))[game_id]


def get_last_game():
    # Could be a part of a class
    last_game_id = 0
    if redis_instance.exists('GameId'):
        last_game_id = redis_instance.get('GameId')
        return get_game_object(last_game_id.decode("utf-8"))

    return None


def create_new_game(player_name):
    # player_name is the first player
    last_game_id = 0
    games = {}
    if redis_instance.exists('GameId'):
        last_game_id = redis_instance.get('GameId').decode("utf-8")
    if redis_instance.exists('Games'):
        games = json.loads(redis_instance.get('Games'))
    new_game_id = str(int(last_game_id)+1)
    new_game = {"X": player_name, "O": None,
                "moves": ["" for x in range(8)]}
    games[new_game_id] = new_game

    redis_instance.set('Games', json.dumps(games))
    redis_instance.set('GameId', new_game_id)

    return new_game_id
