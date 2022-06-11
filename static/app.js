$(document).ready(function () {
    $(".square").click(function () {
        console.log("Square", this.id)
        var json = JSON.stringify({
            data: this.dataset
        });
        console.log(json)
    });
})
function clickHandler(gameId) {
    renderBoard()
    $.ajax({
        url: "http://127.0.0.1:8000/api/getmoves/" + gameId,
        type: "GET",
        success: function (data) {
            var x = JSON.stringify(data);
            console.log(x);
        },
    });
}

function updateMoves() {
    console.log('call updatemoves request to update db')
    // Not necessary to update moves list
    // Instead send index and the player key (X or O) to the backend
    // ["X", "", "O", "", "", ""]

    // $.ajax({
    //     url: "http://127.0.0.1:8000/api/updatemoves/" + gameId,
    //     type: "POST",
    //     data: {},
    //     success: function (data) {
    //         var x = JSON.stringify(data);
    //         console.log(x);
    //     },
    // });
}


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
