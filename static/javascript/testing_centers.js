$(document).ready(function () {
    $.get("/get_testing_centers", function(data) {
        //console.log($.parseJSON(data))
        console.log(data);
    });
});