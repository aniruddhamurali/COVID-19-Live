var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

var currentHr = String(today.getHours()).padStart(2, '0');
var currentMin = String(today.getMinutes()).padStart(2, '0');
var currentSec = String(today.getSeconds()).padStart(2, '0');

today = yyyy + '-' + mm + '-' + dd;
var currentTime = currentHr + ':' + currentMin + ':' + currentSec + 'Z';

console.log(currentTime);

var key = keys.news_key;

var url = 'http://newsapi.org/v2/everything?' +
          'q=+recent+news+on+coronavirus&' +
          'from=' + today + '&' +
          'sortBy=popularity&' +
          'pageSize=30&' +
          'apiKey=' + key;

var req = new Request(url);

fetch(req)
    .then(function(response) {
        var data = response.json();
        return data;
    })
    .then(function(myJson) {
        var articles = myJson.articles;
        
        var news_data = '<div class="container">'
        for (var i = 0; i < articles.length; i++) {
            // article information
            var article_data = articles[i];
            var source = article_data.source.name;
            var author = article_data.author;
            var title = article_data.title;
            var description = article_data.description;
            var time = (article_data.publishedAt).split('T')[1];
            var url = article_data.url;
            var content = article_data.content;

            // calculate time difference
            time = time.split(':');
            var hr = time[0];
            var min = time[1];
            var elapsed;
            if ((currentHr - hr) < 1) {
                elapsed = "" + (currentMin - min) + " minutes ago";
            } else {
                elapsed = "" + (currentHr - hr) + " hours ago";
            }

            if (i % 2 === 0) {
                news_data += '<div class="row">'
            }

            news_data += '<div class="col-sm d-flex">' +
                            '<div class="card flex-fill bg-secondary">' + 
                                '<div class="card-body">' +
                                    '<h5 class="card-title">' + title + '</h5>' + 
                                    '<small>' + source + '  -  ' + elapsed + '</small>' +
                                    '<p class="card-text">' + description + '</p>' +
                                    '<a href=' + '"' + url + '"' + 'class="btn btn-primary" target="_blank">Go to article</a>' +
                                '</div>' +
                            '</div>' +
                         '</div>'

            if (i % 2 == 1) {
                news_data += '</div><br>'
            }
        }
        news_data += '</div>'
        $('#news_data').html(news_data);
    });

