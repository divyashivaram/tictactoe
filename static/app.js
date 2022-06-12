function renderBoard(currentMoves) {
    for (let i = 0; i < currentMoves.length; i++) {
        updateBoard(i, currentMoves[i])
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

// Look for winning move in polling response
// Update winner and loser states based on player key and username

function updateMoves(gameId, playerKey, index) {

    // Not necessary to update moves list
    // Instead send index and the player key (X or O) to the backend
    // ["X", "", "O", "", "", ""]

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
                var response = JSON.stringify(data);
                if (response['changes']) {
                    updateBoard(response['details'][idx], response['details'][key])
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
