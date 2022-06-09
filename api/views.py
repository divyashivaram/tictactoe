# from http.client import HTTPResponse
import json
from venv import create
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render

# connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


def index(request, *args, **kwargs):
    context = {'moves': []}
    return render(request, 'board.html', context)


@api_view(['POST'])
def create_or_join_game(request, *args, **kwargs):
    """
    accepts username in request body and returns a gameId with response
    """

    player_name = json.loads(request.body)['username']
    last_game = get_last_game()

    if last_game is None or last_game['O'] is None:
        game_id = create_new_game(player_name)
        # update_game_id_in_storage()
    else:
        game_id = redis_instance.get('GameId')

    print("ITEM: ", player_name, 'Game ID: ', game_id)

    # TODO: redirect to game page game_id
    return Response(status=200)


@api_view(['GET'])
def get_all_games(request, *args, **kwargs):
    games = json.loads(redis_instance.get('Games'))
    response = {
        'Games': games
    }
    return Response(response, status=200)


@api_view(['POST'])
def update_moves(request, *args, **kwargs):

    # receive game id, player 'X' or 'O', then index
    # Get game object
    # Update moves list and update the game object in redis
    return


def get_last_game():
    # Could be a part of a class
    last_game_id = 0
    if redis_instance.exists('GameId'):
        last_game_id = redis_instance.get('GameId')
        return json.loads(redis_instance.get('Games'))[str(int(last_game_id))]

    return None


def create_new_game(player_name):
    # player_name is the first player
    last_game_id = 0
    if redis_instance.exists('GameId'):
        last_game_id = redis_instance.get('GameId')
    games = json.loads(redis_instance.get('Games'))
    new_game_id = str(int(last_game_id)+1)
    new_game = {"X": player_name, "O": None,
                "moves": ["" for x in range(8)]}
    games[new_game_id] = new_game

    redis_instance.set('Games', json.dumps(games))
    redis_instance.set('GameId', new_game_id)
