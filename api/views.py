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
    game_id = redis_instance.get('GameId')
    games = json.loads(redis_instance.get('Games'))

    response = {
        'GameId': game_id,
        'Games': games[str(int(game_id))]
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


@api_view(['GET'])
def get_items(request, *args, **kwargs):
    # items = {}
    # count = 0
    # for key in redis_instance.keys("*"):
    # items[key.decode("utf-8")] = redis_instance.get(key)
    # count += 1
    gameId = redis_instance.get('GameId')
    games = json.loads(redis_instance.get('Games'))
    print(gameId)
    response = {
        'GameId': gameId,
        'Games': games[str(int(gameId))]
    }
    return Response(response, status=200)


@api_view(['POST'])
def create_item(request, *args, **kwargs):
    item = json.loads(request.body)
    key = list(item.keys())[0]
    value = item[key]

    key = 'Game'

    last_game_id = redis_instance.get('GameId')
    games = json.loads(redis_instance.get('Games'))
    games[str(int(last_game_id)+1)] = create_game(
        'player1', '', ["", "", "", "", "", "", "", "", ""])

    redis_instance.set('Games', json.dumps(games))
    redis_instance.set('GameId', '1')

    response = {
        'msg': f"{key} successfully set to {games}"
    }
    return Response(response, 201)


@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_instance.get(kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_instance.get(kwargs['key'])
            if value:
                redis_instance.set(kwargs['key'], new_value)
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['key']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_instance.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['key']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
