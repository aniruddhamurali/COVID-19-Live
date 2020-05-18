(function() {
    var result = "";
    window.addEventListener('load', function() {
        var form = document.getElementById('needs-validation');
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false || isNaN(parseFloat($('#height').val(), 10)) || isNaN(parseFloat($('#weight').val(), 10))) {
                $('.form-check-label').css({'color':'white'});
                event.preventDefault();
                event.stopPropagation();
            } else {
                $('.form-check-label').css({'color':'white'});
                result = JSON.stringify($(form).serializeArray());
                $.ajax({
                    type: "POST",
                    url: "/get_form_data",
                    contentType: "application/json",
                    data: result,
                    dataType: "json",
                    success: function(response) {
                        console.log(response);
                        var color = "white";
                        if (response >= 75) color = "red";
                        else if (response >= 50) color = "orange";
                        else if (response >= 25) color = "yellow";
                        else color = "green";
                        $('#result').html('<div style="background-color: #0f0f0f; width: 70%; margin: 0 15%; padding: 8px 0; border-radius: 3px;">' +
                                            '<h3 style="color: #1ba0e3;">Your predicted mortality risk is: <h3 style="color: ' + color + '; margin-bottom: 0;">' + response.toFixed(2) + '%</h3></h3>' +
                                          '</div>');
                    },
                    error: function(err) {
                        console.log(err);
                    }
                });
                
                //return false;
                event.preventDefault();
            }
            form.classList.add('was-validated');
            
        }, false);
    }, false);

    
})();