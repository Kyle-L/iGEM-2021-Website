$(document).ready(function() {

    // $('div').each( function(i){
    //     $(this).css('opacity', '0');
    // });

    $('.fadeMeInstantly').each( function(i){
        $(this).animate({'opacity':'1'},500);
    });

    // $('div').each( function(i){
    //     var bottom_of_object = $(this).position().top + ($(this).outerHeight())/8;
    //     var bottom_of_window = $(window).scrollTop() + $(window).height();
    //     if( bottom_of_window > bottom_of_object ){
    //         $(this).css('opacity', '1');
    //     }
    // });

    // $(window).scroll( function(){
    //     $('*').each( function(i){
    //         var bottom_of_object = $(this).position().top + ($(this).outerHeight())/8;
    //         var bottom_of_window = $(window).scrollTop() + $(window).height();
    //         if( bottom_of_window > bottom_of_object ){
    //             $(this).animate({'opacity':'1'},500);
    //         }
    //     });
    // });
});