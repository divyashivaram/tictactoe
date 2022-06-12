function renderBoard(currentMoves) {
    for (let i = 0; i < currentMoves.length; i++) {
        updateBoard(i, currentMoves[i])
        if (currentMoves[i]) {
            disableSquare(i)
        }
    }
}

function updateBoard(id, key) {
    $('#' + id).html(key)
}

function disableSquare(id) {
    $('#' + id).prop('disabled', true);
}

function disableAllSquares() {
    $(".square").prop('disabled', true)
}

function enableSquare(id) {
    $('#' + id).prop('disabled', false);
}


function updateMoves(gameId, playerKey, index) {
    $.ajax({
        url: "http://127.0.0.1:8000/api/updateMoves",
        type: "POST",
        data: { 'gameId': gameId, 'playerKey': playerKey, 'index': index },
        success: function (data) {
            var x = JSON.stringify(data);

        },
    });
}

$(document).ready(function () {
    gameId = $("#board").attr("data-game-id")
    gameObject = $("#board").attr("data-game")
    moves = JSON.parse(gameObject).moves

    renderBoard(moves[moves.length - 1])

    $(".square").click(function () {
        disableAllSquares()
        $(this).prop('disabled', true);
        playerKey = $("#board").attr("data-player-sign")
        index = this.id
        updateBoard(index, playerKey)
        updateMoves(gameId, playerKey, index)
    });
    pollForUpdates(gameId)
})


function enableMoves(lastPlayedKey, currentPlayerKey, moves) {
    if (lastPlayedKey !== currentPlayerKey) {
        for (let i = 0; i <= moves.length; i++) {
            if (moves[i] === "") {
                enableSquare(i)
            }
        }
    }
}

function pollForUpdates() {
    gameId = $("#board").attr("data-game-id")
    currentPlayerKey = $("#board").attr("data-player-sign")


    setInterval(function () {
        $.ajax({
            url: "http://127.0.0.1:8000/api/getmoves/" + gameId,
            type: "GET",
            success: function (data) {
                var response = JSON.parse(JSON.stringify(data))
                if (response['changes'] == true) {
                    lastPlayedKey = response.details.key
                    updateBoard(response.details.idx, lastPlayedKey)
                    disableSquare(response.details.idx)
                    enableMoves(lastPlayedKey, currentPlayerKey, response.mostRecentMove)
                    console.log('Winner', response.winner)
                    if (response.winner) {
                        disableAllSquares()
                    }
                }
            },
        });
    }, 2000);
}
