"use strict";


// ============================================================================
// 共通処理
// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------
// canvasで画像を作成し、ajaxを利用して、サーバーに画像を送る機能
// 

var main_canvas;
var canvas_context;
var oldx = 0,
    oldy = 0,
    x = 0,
    y = 0;
var is_mouse_button_down = false;


// ----------------------------------------------------------------------------
// ページ（body）ロードした時の初期化処理
// 
function initOnLoad() {
    initDrawFunc();
    //他の初期化が必要な関数はここに書く
}

// ----------------------------------------------------------------------------
// 描画機能の初期化
// 
function initDrawFunc() {
    main_canvas = document.getElementById("main_canvas");
    if (main_canvas) {
        main_canvas.addEventListener("touchstart", touchStart, false);
        main_canvas.addEventListener("touchmove", touchMove, false);
        main_canvas.addEventListener("touchend", touchEnd, false);
        main_canvas.addEventListener("mousedown", onMouseDown, false);
        main_canvas.addEventListener("mousemove", onMouseMove, false);
        main_canvas.addEventListener("mouseup", onMouseUp, false);
        canvas_context = main_canvas.getContext("2d");
        canvas_context.strokeStyle = "black";
        canvas_context.lineWidth = 18;
        canvas_context.lineJoin = "round";
        canvas_context.lineCap = "round";
        clearCanvas();
    }
}

// ----------------------------------------------------------------------------
// 
// 
function touchStart(event) {
    is_mouse_button_down = true;
    oldx = event.touches[0].pageX - event.target.getBoundingClientRect().left;
    oldy = event.touches[0].pageY - event.target.getBoundingClientRect().top;
    event.stopPropagation();
}
// ----------------------------------------------------------------------------
// 
// 
function touchMove(event) {
    if (is_mouse_button_down) {
        x = event.touches[0].pageX - event.target.getBoundingClientRect().left;
        y = event.touches[0].pageY - event.target.getBoundingClientRect().top;
        drawLine();
        oldx = x;
        oldy = y;
        event.preventDefault();
        event.stopPropagation();
    }
}
// ----------------------------------------------------------------------------
// 
// 
function touchEnd(event) {
    is_mouse_button_down = false;
    event.stopPropagation();
}
// ----------------------------------------------------------------------------
// マウスが押下検出時の動作
// 
function onMouseDown(event) {
    oldx = event.clientX - event.target.getBoundingClientRect().left;
    oldy = event.clientY - event.target.getBoundingClientRect().top;
    is_mouse_button_down = true;
}
// ----------------------------------------------------------------------------
// マウスが移動検出時の動作
// 
function onMouseMove(event) {
    if (is_mouse_button_down) {
        x = event.clientX - event.target.getBoundingClientRect().left;
        y = event.clientY - event.target.getBoundingClientRect().top;
        drawLine();
        oldx = x;
        oldy = y;
    }
}
// ----------------------------------------------------------------------------
// 
// 
function onMouseUp(event) {
    is_mouse_button_down = false;
}
// ----------------------------------------------------------------------------
// 線を描画します
// 
function drawLine() {
    canvas_context.beginPath();
    canvas_context.moveTo(oldx, oldy);
    canvas_context.lineTo(x, y);
    canvas_context.stroke();
}
// ----------------------------------------------------------------------------
// Canvasをクリアします
// 
function clearCanvas() {
    canvas_context.fillStyle = "rgb(255,255,255)";
    canvas_context.fillRect(0, 0, main_canvas.getBoundingClientRect().width, main_canvas.getBoundingClientRect().height);

    $.ajax({
            type: "POST",
            url: "/clearcanvas",
            data: {

            }
        })
        .done((data) => {
            $('#answer').html('');
        });
}

// ============================================================================
// Chainer MNIST
// ----------------------------------------------------------------------------
// 
function sendDrawnImage2Chainer() {
    //まず結果を非表示にしておきます。
    $('#answer').html('');
    var image = document.getElementById("main_canvas").toDataURL('image/png');
    image = image.replace('image/png', 'image/octet-stream');
    $.ajax({
            type: "POST",
            url: "/chainer",
            data: {
                "image": image
            }
        })
        .done((data) => {
            //結果が返ってきたら、表示します。
            $('#answer').html('<span class="answer-text">' + data['result'] + '</span>');
        });
}



// ============================================================================
// Chainer Dogs & Cats
// ----------------------------------------------------------------------------
//
function sendDrawnImageChainerDogsCats() {
    //まず結果を非表示にしておきます。
    $('#answer').html('');
    var image = document.getElementById("main_canvas").toDataURL('image/png');
    image = image.replace('image/png', 'image/octet-stream');
    $.ajax({
            type: "POST",
            url: "/dogscats",
            data: {
                "image": image
            }
        })
        .done((data) => {
            //結果が帰ってきたら、表示します。
            $('#answer').html('<span class="answer-text">' + data['result'] + '</span>');
        });
}

// ============================================================================
// Chainer Dogs & Cats 写真アップロード判別
// ----------------------------------------------------------------------------
//
function getUploadDogscatsResult() {
    //まず結果を非表示にしておきます。
    $('#answer').html('');
    $.ajax({
            type: "GET",
            url: "/dogscatsuploadresult",
        })
        .done((data) => {
            //結果が帰ってきたら、表示します。
            $('#answer').html('<span class="flower-answer-text">' + data['result'] + '</span>');
        });
}

// ============================================================================
// Keras MNIST
// ----------------------------------------------------------------------------
//
function sendDrawnImage2Keras() {
    //まず結果を非表示にしておきます。
    $('#answer').html('');
    var image = document.getElementById("main_canvas").toDataURL('image/png');
    image = image.replace('image/png', 'image/octet-stream');
    $.ajax({
            type: "POST",
            url: "/keras",
            data: {
                "image": image
            }
        })
        .done((data) => {
            //結果が帰ってきたら、表示します。
            $('#answer').html('<span class="answer-text">' + data['result'] + '</span>');
        });
}

// ============================================================================
// TensorFlow Flower 手書き判別
// ----------------------------------------------------------------------------
//
function sendDrawnFlowerImage() {
    //まず結果を非表示にしておきます。
    $('#answer').html('');
    var image = document.getElementById("main_canvas").toDataURL('image/png');
    image = image.replace('image/png', 'image/octet-stream');
    $.ajax({
            type: "POST",
            url: "/flower",
            data: {
                "image": image
            }
        })
        .done((data) => {
            //結果が帰ってきたら、表示します。
            $('#answer').html('<span class="flower-answer-text">' + data['result'] + '</span>');
        });
}

// ============================================================================
// TensorFlow Flower 写真アップロード判別
// ----------------------------------------------------------------------------
//
function getUploadFlowerResult() {
    //まず結果を非表示にしておきます。
    $('#answer').html('');
    $.ajax({
            type: "GET",
            url: "/floweruploadresult",
        })
        .done((data) => {
            //結果が帰ってきたら、表示します。
            $('#answer').html('<span class="flower-answer-text">' + data['result'] + '</span>');
        });
}