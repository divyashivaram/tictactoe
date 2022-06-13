from .models import Redis
import json

redis = Redis()


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
