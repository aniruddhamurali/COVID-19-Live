(function() {
    var result = "";
    window.addEventListener('load', function() {
        var form = document.getElementById('needs-validation');
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            } else {
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
                        $('#result').html('<h2>Your predicted mortality risk is: <h2 style="color: ' + color + '">' + response.toFixed(2) + '%</h2></h2>');
                    },
                    error: function(err) {
                        console.log(err);
                    }
                });
                
                event.preventDefault();
            }
            form.classList.add('was-validated');
            
        }, false);
    }, false);

    
})();