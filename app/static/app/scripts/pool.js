$(document).ready(function () {
    $('#submitBtn').mouseover(function () {
        $(this).css('color', 'blue');
    });

    $('#submitBtn').mouseout(function () {
        $(this).css('color', ''); 
    });

    $('input[type="text"]').focus(function () {
        $(this).css('background-color', 'lightyellow');
    });

    $('input[type="text"]').blur(function () {
        $(this).css('background-color', '');
    });
});
