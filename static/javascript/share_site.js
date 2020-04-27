$(document).ready(function() {
    $('.fa-facebook-square').click(function() {
        FB.ui({
            display: 'popup',
            method: 'share',
            href: 'https://developers.facebook.com/docs/',
        }, function(response){});
    });
});