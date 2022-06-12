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
    // $(this).prop('disabled', true);
    $('#' + id).prop('disabled', true);
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
        disableSquare(this.id)
        $(this).prop('disabled', true);
        playerKey = $("#board").attr("data-player-sign")
        index = this.id
        updateBoard(index, playerKey)
        updateMoves(gameId, playerKey, index)
    });
    pollForUpdates(gameId)
})


function pollForUpdates() {
    gameId = $("#board").attr("data-game-id")

    setInterval(function () {
        $.ajax({
            url: "http://127.0.0.1:8000/api/getmoves/" + gameId,
            type: "GET",
            success: function (data) {
                var response = JSON.parse(JSON.stringify(data))
                if (response['changes'] == true) {
                    updateBoard(response.details.idx, response.details.key)
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
