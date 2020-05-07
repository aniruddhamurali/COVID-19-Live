$(document).ready(function () {
    var first = false;
    var j = 0;
    var cards = [];

    $.get("/get_testing_centers", function(data) {
        //console.log($.parseJSON(data))
        results = $.parseJSON(data);
        var htmlResult = '';
        //var cards = [];
        for (var i = 0; i < results.length; i++) {
            htmlResult += '<a>'
            name = results[i].name;
            details = results[i].details;
            appointment = results[i].appointment;
            referral = results[i].referral;
            testing = results[i].testing;
            driving = results[i].drive_through;
            instructions = results[i].instructions;
            link = results[i].link;

            htmlResult += '<h3>' + name + '</h3>' +
                          '<h5>' + details + '</h5>' +
                          '<table>' +
                            '<tr>' +
                                '<td>' + appointment + '</td>' +
                                '<td>' + referral + '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<td>' + testing + '</td>' +
                                '<td>' + driving + '</td>' +
                            '</tr>' +
                          '</table>' + 
                          '<br>' +
                          '<p>' + instructions + '</p>' +
                          '</a>'

            // new code
            cards.push(htmlResult);
            htmlResult = '';
        }
        //console.log(data);
        //$('.scrollmenu').html(htmlResult);
        console.log(cards);
        if (first == false) {
            $('#card').html(cards[0]);
            first = true;
            j = 1;
        }
    });

    $("#right").click(function() {
        console.log(j);
        $('#card').html(cards[j]);
        if (j == cards.length) j = 0;
        else j += 1;    
    });

    $("#left").click(function() {
        console.log(j);
        $('#card').html(cards[j]);
        if (j == 0) j = cards.length - 1;
        else j -= 1;    
    });
});