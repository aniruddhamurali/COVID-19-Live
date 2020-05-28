$(document).ready(function () {
    var coords = {lat: "", lon: ""};
    var first = false;
    var j = 0;
    var cards = [];

    // When called, get user location and display nearby testing centers
    function showPosition(position) {
        coords.lat = (position.coords.latitude).toString();
        coords.lon = (position.coords.longitude).toString();
        var result = JSON.stringify(coords);

        $.ajax({
            type: "POST",
            url: "/get_testing_centers",
            contentType: "application/json",
            data: result,
            dataType: "json",
            success: function(response) {
                //var results = $.parseJSON(response);
                var results = response;
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

                    htmlResult += '<h4>' + name + '</h4>' +
                                '<h6>' + details + '</h6>' +
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
                                //'<p>' + instructions + '</p>' +
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
            },
            error: function(err) {
                console.log(err);
                $('#card').html("<p>Unable to load data. Most likely a probably with your connection.</p>");
            }
        });
    }

    // Function to get user location
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        } else { 
            $('#loc').html("Geolocation is not supported by this browser.");
        }
    }

    getLocation();

    /*
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

            htmlResult += '<h4>' + name + '</h4>' +
                          '<h6>' + details + '</h6>' +
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
    */

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