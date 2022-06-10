# from http.client import HTTPResponse
from .forms import NameForm
import json
from venv import create
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


def index(request, *args, **kwargs):
    context = {'moves': []}
    form = NameForm(request.POST)
    print("FORM: ", request)
    return render(request, 'landing.html', context)


@api_view(['POST'])
def create_or_join_game(request, *args, **kwargs):
    form = NameForm(request.POST)
    username = form.data['your_name']
    player_name = username
    last_game = get_last_game()

    if last_game is None or last_game['O'] is not None:
        game_id = create_new_game(player_name)
        # update_game_id_in_storage()
    else:
        game_id = redis_instance.get('GameId')

    game_id = str(int(game_id))
    # add user to 'O'
    # TODO: redirect to game page game_id
    return redirect('get_game', game_id=game_id)


@api_view(['GET'])
def render_game(request, game_id):
    context = {'moves': get_game_object(game_id)['moves']}
    # TODO: Handle error here. Page does not exist, throw exception etc
    # example:
    # from django.http import Http404
    # try:
    #     board = board.objects.get(pk=game_id)
    # except board.DoesNotExist:
    #     raise Http404("Game does not exist")
    return render(request, 'board.html', context)


def get_game_object(game_id):
    return json.loads(redis_instance.get('Games'))[str(int(game_id))]


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
    game_object = games[str(int(game_id))]
    game_object['moves'] = moves
    # receive game id, player 'X' or 'O', then index
    # Get game object
    # Update moves list and update the game object in redis
    return


def add_second_player(player_name, game_id):

    return


def get_last_game():
    # Could be a part of a class
    last_game_id = 0
    if redis_instance.exists('GameId'):
        last_game_id = redis_instance.get('GameId')
        return get_game_object(last_game_id)

    return None


def create_new_game(player_name):
    # player_name is the first player
    last_game_id = 0
    games = {}
    if redis_instance.exists('GameId'):
        last_game_id = redis_instance.get('GameId')
    if redis_instance.exists('Games'):
        games = json.loads(redis_instance.get('Games'))
    new_game_id = str(int(last_game_id)+1)
    new_game = {"X": player_name, "O": None,
                "moves": ["" for x in range(8)]}
    games[new_game_id] = new_game

    redis_instance.set('Games', json.dumps(games))
    redis_instance.set('GameId', new_game_id)

    return new_game_id
