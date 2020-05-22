var InputNumber = $('#number')
var InputUrl = $('#url')
var videosubInputId = $('#videosub-input-id')

$('.update-btn').click(function(){
    var videosubId = $(this).attr('data-id');
    var videosubUrl = $(this).attr('data-url');
    var videosubNumber = parseInt($(this).attr('data-number'));

    InputNumber.val(videosubNumber);
    InputUrl.val(videosubUrl);
    videosubInputId.val(videosubId);

});




