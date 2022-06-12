function renderBoard(currentMoves) {
    for (let i = 0; i < currentMoves.length; i++) {
        updateBoard(i, currentMoves[i])
        if (currentMoves[i]) {
            disableSquare(i)
        }
    }
}

function clickHandler(gameId) {
    $.ajax({
        url: "http://127.0.0.1:8000/api/getmoves/" + gameId,
        type: "GET",
        success: function (data) {
            var x = JSON.stringify(data);
        },
    });
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

// Look for winning move in polling response
// Update winner and loser states based on player key and username

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
                }
            },
        });
    }, 2000);
}



// After polling call update board again

// Get element by id and update the value
// ('#0').attr('value', 'X')

// function ajaxReq() {
//     setInterval(function () {
//         $.ajax({
//             url: "https://jsonplaceholder.typicode.com/todos/1",
//             type: "GET",
//             success: function (data) {
//                 var x = JSON.stringify(data);
//                 console.log(x);
//             },
//         });
//     }, 2000);
// }
