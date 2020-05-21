var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

var currentHr = String(today.getHours()).padStart(2, '0');
var currentMin = String(today.getMinutes()).padStart(2, '0');
var currentSec = String(today.getSeconds()).padStart(2, '0');

today = yyyy + '-' + mm + '-' + dd;
var currentTime = currentHr + ':' + currentMin + ':' + currentSec + 'Z';


var key = keys.news_key;
var count = 30;
const proxyurl = "https://cors-anywhere.herokuapp.com/";

var url = 'https://newsapi.org/v2/everything?' +
          'q=+recent+news+on+coronavirus&' +
          'from=' + today + '&' +
          'sortBy=popularity&' +
          'pageSize=' + count + '&' +
          'apiKey=' + key;

var req = new Request(proxyurl + url);

// Get more articles
$('#more').click(function() {
    count += 30;
    var url = 'https://newsapi.org/v2/everything?' +
          'q=+recent+news+on+coronavirus&' +
          'from=' + today + '&' +
          'sortBy=popularity&' +
          'pageSize=' + count + '&' +
          'apiKey=' + key;
    var req = new Request(url);
    fetch(req)
        .then(function(response) {
            var data = response.json();
            return data;
        })
        .then(function(myJson) {
            var articles = myJson.articles;
            
            //var news_data = '<div class="container text-center" style="width: 100%;">';
            news_data = '<div>';
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

                console.log(source);

                news_data += '<div class="card flex-fill">' + 
                            '<div class="card-body">' +
                                '<h5 class="card-title">' + title + '</h5>' + 
                                '<small>' + source + '  -  ' + elapsed + '</small>' +
                                '<p class="card-text">' + description + '</p>' +
                            '</div>' +
                            '<div>' + 
                                '<a href=' + '"' + url + '"' + 'class="" target="_blank">Go to article</a>' + 
                            '</div>' +
                            '<br>' +
                         '</div>';
                
                /*news_data += '<div class="card flex-fill">' + 
                                '<div class="card-body">' +
                                    '<h5 class="card-title">' + title + '</h5>' + 
                                    '<small>' + source + '  -  ' + elapsed + '</small>' +
                                    '<p class="card-text">' + description + '</p>' +
                                    '<a href=' + '"' + url + '"' + 'class="btn btn-primary" target="_blank">Go to article</a>' +
                                '</div>' +
                            '</div>';*/
            }

            news_data += '</div>';
            $('#news_data').html(news_data);
        });
});


// Initial display
fetch(req)
    .then(function(response) {
        var data = response.json();
        return data;
    })
    .then(function(myJson) {
        var articles = myJson.articles;
        
        //var news_data = '<div class="text-center">';
        var news_data = '<div>';
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
                elapsed = "" + Math.abs((currentMin - min)) + " minutes ago";
            } else {
                elapsed = "" + Math.abs((currentHr - hr)) + " hours ago";
            }
            
            news_data += '<div class="card flex-fill">' + 
                            '<div class="card-body">' +
                                '<h5 class="card-title">' + title + '</h5>' + 
                                '<small>' + source + '  -  ' + elapsed + '</small>' +
                                '<p class="card-text">' + description + '</p>' +
                            '</div>' +
                            '<div>' + 
                                '<a href=' + '"' + url + '"' + 'class="" target="_blank">Go to article</a>' + 
                            '</div>' +
                            '<br>' +
                         '</div>';
        }

        news_data += '</div>';
        $('#news_data').html(news_data);
    });

