$(function() {
    /*$.ajax({
        url: '/api/info',
        success: function(data) {
            console.log('get info');
            $('#info').html(JSON.stringify(data, null, '   '));
            $('#description').html(data['description']);
        }
    });*/
 
    $('#calc').click(function() {
        $('#info').css('display', "none");
        $('#description').css('display', "none");
        //console.log(url);
        /*var dic={"wires":2,"cols":[["h"],["c","x"],["m","m"]]};
        var img=new Image();
        img.src="/plot.png"
        document.getElementById('results').appendChild(img);*/
        $.ajax({

            url : '/api/calc?a=' + JSON.stringify(dic) ,
            success: function(data) {
                //$('#diracNotation').html("diracNotation : "+data["diracNotation"]);
                //$('#matrixRepresentation').html("matrixRepresentation : "+JSON.stringify(data["matrixRepresentation"]));
            }
        });
    });
})