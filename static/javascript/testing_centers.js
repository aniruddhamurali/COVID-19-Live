$(document).ready(function () {
    $.get("/get_testing_centers", function(data) {
        //console.log($.parseJSON(data))
        results = $.parseJSON(data);
        var htmlResult = '';
        for (var i = 0; i < results.length; i++) {
            htmlResult += '<div style="width: 50%;>"'
            name = results[i].name;
            details = results[i].details;
            appointment = results[i].appointment;
            referral = results[i].referral;
            testing = results[i].testing;
            driving = results[i].drive_through;
            instructions = results[i].instructions;
            link = results[i].link;
            //console.log(results[i]);
            console.log(name);
            htmlResult += '<h3>' + name + '</h3>' +
                          '<h5>' + details + '</h5>' +
                          '<p>' + appointment + '</p>' +
                          '<p>' + referral + '</p>' +
                          '<p>' + testing + '</p>' +
                          '<p>' + driving + '</p>' +
                          '<p>' + 'Instructions: ' + instructions + '</p>' +
                          '</div>'
        }
        //console.log(data);
        $('#testing_centers').html(htmlResult);
    });
});