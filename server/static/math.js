$(function() {
    $.ajax({
        url: '/api/info',
        success: function(data) {
            console.log('get info');
            $('#info').html(JSON.stringify(data, null, '   '));
            $('#description').html(data['description']);
        }
    });
 
    $('#calc').click(function() {
        $('#info').css('display', "none");
        $('#description').css('display', "none");
        //console.log(url);
        $.ajax({
            url : '/api/calc?a=' + document.getElementById('a').value ,
            success: function(data) {
                $('#add').html(JSON.stringify(data,null,'   '));
            }
        });
    });
})