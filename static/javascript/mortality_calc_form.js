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
                console.log(result);
                $.ajax({
                    type: "POST",
                    url: "/get_form_data",
                    contentType: "application/json",
                    data: result,
                    dataType: "json",
                    success: function(response) {
                        console.log(response);
                    },
                    error: function(err) {
                        console.log(err);
                    }
                });
                /*
                $.post( "/get_form_data", {
                    javascript_data: result 
                });*/
                event.preventDefault();
            }
            form.classList.add('was-validated');
            
        }, false);
    }, false);

    
})();