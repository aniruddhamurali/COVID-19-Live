
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;

var key = keys.news_key;

var url = 'http://newsapi.org/v2/everything?' +
          'q=Coronavirus&COVID-19&' +
          'from=' + today + '&' +
          'sortBy=popularity&' +
          'apiKey=' + key;

var req = new Request(url);

fetch(req)
    .then(function(response) {
        console.log(response.json());
    })
