from .forms import NameForm
import json
import redis
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .services import *


@api_view(['GET'])
def index(request, *args, **kwargs):
    return render(request, 'landing.html', {})


@api_view(['POST'])
def create_or_join_game(request, *args, **kwargs):
    # TODO: Call this join game
    # TODO: Now call create or join game in services.py that logic should not be here

    # Potential bug:
    # Usecase: User 1 has a certain user name. User 2 joins the game with the same user name
    # When user 2 makes a move, 'fetch key by value' would return 'X' instead of 'O' and user 2 would end up playing on behalf of user 1
    # The current logic only works when both users have different usernames

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


@api_view(['GET'])
def get_moves(request, game_id):
    # TODO: Mopve all the logic to services.py
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
