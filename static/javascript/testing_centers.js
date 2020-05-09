$(document).ready(function () {
    var first = false;
    var j = 0;
    var cards = [];

    $.get("/get_testing_centers", function(data) {
        var results = $.parseJSON(data);
        var htmlResult = '';
        for (var i = 0; i < results.length; i++) {
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
                          '<div class="divider"></div>' +
                          '<table>' +
                            '<tr>' +
                                '<td class="bg-info">' + appointment + '</td>' +
                                '<td class="bg-info">' + referral + '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<td class="bg-info">' + testing + '</td>' +
                                '<td class="bg-info">' + driving + '</td>' +
                            '</tr>' +
                          '</table>' + 
                          '<br>' +
                          '<p>' + instructions + '</p>' +
                          '<a href=' + '"' + link + '"' + 'class="btn btn-primary" target="_blank">Go to website</a>' +
                          '</a>'

            cards.push(htmlResult);
            htmlResult = '';
        }

        if (first == false) {
            $('#card').html(cards[0]);
            first = true;
            j = 1;
        }
    });

    $("#right").click(function() {
        $('#card').html(cards[j]);
        if (j == cards.length) j = 0;
        else j += 1;    
    });

    $("#left").click(function() {
        $('#card').html(cards[j]);
        if (j == 0) j = cards.length - 1;
        else j -= 1;    
    });
});