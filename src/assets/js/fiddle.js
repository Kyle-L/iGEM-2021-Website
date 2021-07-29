$(document).ready(function() {

    $('.fadeMeInstantly').each( function(i){
        $(this).animate({'opacity':'1'},500);
    });

    $('.fadeMe').each( function(i){
        var bottom_of_object = $(this).position().top + ($(this).outerHeight())/3;
        var bottom_of_window = $(window).scrollTop() + $(window).height();
        if( bottom_of_window > bottom_of_object ){
            $(this).css('opacity', '1');
        }
    });

    $(window).scroll( function(){
        $('.fadeMe').each( function(i){
            var bottom_of_object = $(this).position().top + ($(this).outerHeight())/3;
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            if( bottom_of_window > bottom_of_object ){
                $(this).animate({'opacity':'1'},500);
            }
        });
    });
});