var current_page = 0;

var page_list = {
    0:"container-1",
    1:"container-2",
}

var GAME_END_TEXT={
    'win' : 'You Won!!! :)',
    'loss': 'You Loss :(',
    'tie' : 'Tie'
}

// # board grid
let history = {}
let num_fill_box = 0
let state = []
let current_player = 0;
const board_size = 5;
const MATCH_COUNT = 4
let last_move = null;
let bot_player_num = 2;
let game_status = { 'tie': false, 'end': false, 'win': -1 };

let playing_with_bot = false
let player_1_score = 0
let player_2_score = 0
// console.log($('.btn'))
$(document).ready(()=>{
    change_page(0)
    private_socket = io.connect('http://' + document.domain + ':' + location.port + '/private');

    reset_board()

    private_socket.on("server response", (data) => {
        $(`.lds-ellipsis`).css('display', 'none')
        console.log(data)
        state[parseInt(data["action"])] = current_player + 1;
        history[num_fill_box] = current_player;
        last_move = parseInt(data["action"])
        $(`#box-${data["action"]}`).html((current_player == 0) ? "O" : "X")
        current_player = (current_player + 1) % 2
        num_fill_box += 1

        game_status = is_game_end(state)

        if (game_status.end) {
            $(`#reset_btn`).css('pointer-events', 'auto');
            $(`#reset_btn`).css('opacity', '1');
            if (game_status.tie) {
                $(`#game_end_state`).css('display', 'flex');
                $(`#game_end_text`).html(GAME_END_TEXT.tie)
            }
            else if (game_status.win == 1) {
                $(`#game_end_state`).css('display', 'flex');
                $(`#game_end_text`).html(GAME_END_TEXT.win);
                player_1_score += 1;
                $(`#score_of_human`).html(player_1_score)
            }
            else if (game_status.win == 2) {
                $(`#game_end_state`).css('display', 'flex');
                $(`#game_end_text`).html(GAME_END_TEXT.loss);
                player_2_score += 1;
                $(`#score_of_bot`).html(player_2_score)
            }
        }
    })
})

$(`#alpha_zero_btn`).click(()=>{
    change_page(1);
    bot_player_num = 1
})
$(`#second_btn`).click(()=>{
    change_page(1);
    bot_player_num = 2;
})

$(`#reset_btn`).click(()=>{
    reset_board();
})

$(`#game_end_state`).click(()=>{
    $(`#game_end_state`).css('display' , 'none');
})

let change_page = (page_index)=>{
    var validate_page_index = page_index >= 0 && page_index <= Object.keys(page_list).length && page_index;
    console.log(validate_page_index)
    if(validate_page_index !== false){
        current_page = page_index;
        for(var item in page_list){
            console.log(typeof item)
            if(parseInt(item) === validate_page_index){
                $(`#${page_list[item]}`).css("display" , "flex");
                $
            }else{
                $(`#${page_list[item]}`).css("display" , "none");
            }
        }
        
    }
}
function reset_board() {
    current_player = 0
    history = {}
    state = []
    game_status = { 'tie': false, 'end': false, 'win': -1 };
    $(`#game_end_state`).css('display' , 'none');
    $(".grid-container").empty();
    
    let coloum_formate = "";
    for (var i = 0; i < board_size; i++) {
        coloum_formate += "auto "
    }
    $(`#reset_btn`).css('pointer-events', 'none');
    $(`#reset_btn`).css('opacity', '0');
    $(".grid-container").css("grid-template-columns", coloum_formate)
    for (var i = 0; i < board_size * board_size; i++) {
        state[i] = 0;
        var append_div_class = "grid-item"
        var x = Math.floor(i / board_size)
        var y = i % board_size
        if (x == 0) append_div_class += " remove-top-border"
        if (y == 0) append_div_class += " remove-left-border"
        if (x == (board_size - 1)) append_div_class += " remove-bottom-border"
        if (y == (board_size - 1)) append_div_class += " remove-right-border"

        $(".grid-container").append(`<div id = "box-${i}"class="${append_div_class}"></div>`)

    }

    $(".grid-item").click(function () {
        console.log($(this).html() == "")
        if ($(this).html() == "" && current_player != bot_player_num && game_status.end == false) {
            $(this).html((current_player == 0) ? "O" : "X")
            let id_str = $(this).attr('id')
            let id = parseInt(id_str.split("-")[1])
            last_move = id
            state[id] = current_player + 1
            history[num_fill_box] = parseInt(id_str.split("-")[1])
            num_fill_box += 1

            current_player = (current_player + 1) % 2;
            game_status= is_game_end(state)
            if(game_status.end){
                $(`#reset_btn`).css('pointer-events', 'auto');
                $(`#reset_btn`).css('opacity', '1');
                if (game_status.tie){
                    $(`#game_end_state`).css('display' , 'flex');
                    $(`#game_end_text`).html(GAME_END_TEXT.tie)
                }
                else if(game_status.win == 1){
                    $(`#game_end_state`).css('display' , 'flex');
                    $(`#game_end_text`).html(GAME_END_TEXT.win);
                    player_1_score+=1;
                    $(`#score_of_human`).html(player_1_score)
                }
                else if(game_status.win == 2){
                    $(`#game_end_state`).css('display' , 'flex');
                    $(`#game_end_text`).html(GAME_END_TEXT.loss);
                    player_2_score+=1;
                    $(`#score_of_bot`).html(player_2_score)
                }
            }else{
                $(`.lds-ellipsis`).css('display', 'inline-block')
                console.log("REQUEST SEND")
                private_socket.emit('send state', { "board_size": board_size, "board_state": state, "current_player": current_player, "last_move": last_move })
            }
            // console.log(state)
            // console.log("REQUEST SEND")
            // private_socket.emit('send state', { "board_size": board_size, "board_state": state, "current_player": current_player, "last_move": last_move })
        }
    })
}


function is_game_end(state){

    var status_of_board = state.find(element => element == 0);

    if(typeof status_of_board == "undefined"){
        return {'tie': true , 'end': true,  'win' : -1}
    }
    console.log(status_of_board)
    for (let index = 0; index < state.length; index++) {

        
        let player = state[index];

        if (player==0) continue

        // console.log(index)

        // HORIZONTAL
        if ( (index%board_size) <=  (board_size - MATCH_COUNT) ){
            var HORIZONTAL = false;
            for(var i=0; i<MATCH_COUNT; i++){
                // console.log(player , state[i])
                if(player == state[index + i]){
                    HORIZONTAL = true;
                }else{
                    HORIZONTAL = false;
                    break;
                }
            }
            if(HORIZONTAL){
                console.log("Okay Got it HORIZONTAL")
                return { 'tie': false, 'end': true, 'win': player}
            }
        }
        
        
        // VERTICAL
        
        if ( Math.floor(index / board_size) <= board_size - MATCH_COUNT) {
            var VERTICAL = false;
            for (var i = 0, j=0; i < MATCH_COUNT; i++,  j+=board_size) {
                // console.log(player, state[j])
                if (player === state[index + j]) {
                    VERTICAL = true;
                } else {
                    VERTICAL = false;
                    break;
                }
            }
            if (VERTICAL) {
                console.log("Okay Got it VERTICAL")
                return { 'tie': false, 'end': true, 'win': player}
            }
        }
        
        // RIGHT DIAGONAL

        if (Math.floor(index / board_size) <= board_size - MATCH_COUNT && index % board_size <= board_size - MATCH_COUNT) {
            var R_DIAGONAL = false;
            for (var i = 0, j = 0; i < MATCH_COUNT; i++, j += board_size + 1) {
                // console.log(player, state[j])
                if (player === state[index + j]) {
                    R_DIAGONAL = true;
                } else {
                    R_DIAGONAL = false;
                    break;
                }
            }
            if (R_DIAGONAL) {
                console.log("Okay Got it R_DIAGONAL")
                return { 'tie': false, 'end': true, 'win': player}
            }
        }
        
        // LEFT DIAGONAL
        
        if (Math.floor(index / board_size) <= board_size - MATCH_COUNT && Math.floor(index % board_size) >= board_size - MATCH_COUNT) {
            var L_DIAGONAL = false;
            for (var i = 0, j = 0; i < MATCH_COUNT; i++, j += board_size - 1) {
                // console.log(player, state[j])
                if (player === state[index + j]) {
                    L_DIAGONAL = true;
                } else {
                    L_DIAGONAL = false;
                    break;
                }
            }
            if (L_DIAGONAL) {
                console.log("Okay Got it L_DIAGONAL")
                return { 'tie': false, 'end': true, 'win': player}
            }
        }
        
    }
    return { 'tie': false, 'end': false, 'win': -1}
}