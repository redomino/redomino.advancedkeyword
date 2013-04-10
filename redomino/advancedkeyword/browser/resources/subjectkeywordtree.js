(function ($){

$(document).ready(function (){
    $('.subjectTree > ul').keywordtree('#subject').collapsedtree();

    $('.subjectTree ul').each(function (){
        $(this).children().children(':checkbox').shiftcheckbox();
    });


});
}(jQuery));
