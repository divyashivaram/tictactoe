from .forms import NameForm
import json
# from venv import create
# from django.conf import settings
import redis
from rest_framework.decorators import api_view
# from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Redis

redis = Redis()


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
    else:
        game_id = redis.read('GameId').decode("utf-8")
        add_second_player(player_name, game_id)

    # redirecting with a query param and an argument. Hence constructing the redirect url right away
    return redirect('{}?player_name={}'.format(reverse('get_game', args=[game_id]), player_name))


def get_key(dict, val):
    """get_key

    Args:
        dict (_dict_): python dictionary
        val (_any_): value to look up

    Returns:
        _any_: returns the respective key or None
    """

    for key, value in dict.items():
        if val == value:
            return key
    return None


@api_view(['GET'])
def render_game(request, *args, **kwargs):
    player_name = str(request.GET.get('player_name', None))
    game = get_game_object(kwargs['game_id'])

    # If player name isn't found it means it is not a redirect, throw authorization error or something?

    context = {
        'game': json.dumps(game),
        'game_id': kwargs['game_id'],
        'player_sign': get_key(game, player_name)}

    # TODO: Handle error here. Page does not exist, throw exception etc
    # example:
    # from django.http import Http404
    # try:
    #     board = board.objects.get(pk=game_id)
    # except board.DoesNotExist:
    #     raise Http404("Game does not exist")
    return render(request, 'board.html', context)


def get_updated_move(list1, list2):
    """
    two lists of same length
    There can only be one different element
    Hence early exit
    List 2 is the latest in this case
    """
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return {'key': list1[i], 'idx': i}
    return None


@api_view(['GET'])
def get_moves(request, game_id):
    games = json.loads(redis.read('Games'))
    game = games[str(game_id)]
    moves = game['moves']
    updates = None
    response = {'changes': False, 'details': updates,
                'mostRecentMove': moves[-1], 'winner': None}

    if len(moves) > 1:
        last_move = moves[-1]
        prev_move = moves[len(moves)-2]
        updates = get_updated_move(last_move, prev_move)
    if updates is not None:
        response['changes'] = True
        response['details'] = updates
        winner = calculate_winner(moves[-1])
        if winner is not None:
            response['winner'] = winner
    # Fetch moves and game object and return
    return JsonResponse(response)


@api_view(['GET'])
def get_all_games(request, *args, **kwargs):
    games = json.loads(redis.read('Games'))
    response = {
        'Games': games
    }
    return Response(response, status=200)


@api_view(['POST'])
def update_moves(request, *args, **kwargs):
    game_id = request.POST['gameId']
    player_key = request.POST['playerKey']
    index_to_update = request.POST['index']

    games = json.loads(redis.read('Games'))
    game = games[game_id]
    moves_copy = game['moves'][-1].copy()
    moves_copy[int(index_to_update)] = player_key
    game['moves'].append(moves_copy)
    redis.write('Games', json.dumps(games))
    return Response(status=200)


def add_second_player(player_name, game_id):
    games = json.loads(redis.read('Games'))
    current_game = games[game_id]
    current_game['O'] = player_name
    redis.write('Games', json.dumps(games))


def get_game_object(game_id):
    return json.loads(redis.read('Games'))[game_id]


def get_last_game():
    # Could be a part of a class
    last_game_id = 0
    if redis.peek('GameId'):
        last_game_id = redis.read('GameId')
        return get_game_object(last_game_id.decode("utf-8"))

    return None


def create_new_game(player_name):
    # player_name is the first player
    last_game_id = 0
    games = {}
    if redis.peek('GameId'):
        last_game_id = redis.read('GameId').decode("utf-8")
    if redis.peek('Games'):
        games = json.loads(redis.read('Games'))
    new_game_id = str(int(last_game_id)+1)
    new_game = {"X": player_name, "O": None,
                "moves": [["" for x in range(9)]]}
    games[new_game_id] = new_game

    redis.write('Games', json.dumps(games))
    redis.write('GameId', new_game_id)

    return new_game_id


def calculate_winner(latest_move):
    winning_moves = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for row in winning_moves:
        [a, b, c] = row
        if (latest_move[a] and latest_move[a] == latest_move[b] and latest_move[b] == latest_move[c]):
            return latest_move[a]

    return None
