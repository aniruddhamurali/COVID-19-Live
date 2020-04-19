Papa.parse("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})

function formatDate() {
    var d = new Date()
    d.setDate(d.getDate() - 1);
    var month = '' + (d.getMonth() + 1)
    var day = '' + d.getDate()
    var year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

function displayHTMLTable(results) {
     // create a date object using Date constructor 
    //var dateObj = new Date(); 
    // subtract one day from current time                           
    //dateObj.setDate(dateObj.getDate() - 1);

    var date = formatDate();
    var data = results.data;

    i = data.length - 1;
    if (data[i]["Date"] === "") i -= 1;
    var row = data[i];
    d = row["Date"];
    console.log(date);

    var table_data = '<table class="table table-bordered table-sm table-hover">';
    for (var count = 0; count < data.length; count++) {
        var cell_data = Object.keys(data[count]).map(function(key){
            return data[count][key];
        });

        if (count === 0) { 
            table_data += '<thead class="thead-dark">' + 
                            '<th>' + 'Country' + '</th>' +
                            '<th>' + 'Confirmed' + '</th>' +
                            '<th>' + 'Recovered' + '</th>' + 
                            '<th>' + 'Deaths' + '</th>' +
                          '</thead>';
        } else if (cell_data[0] !== d) {
            continue;
        } else {
            table_data += '<tr>';
            // Exclude data and percent
            for (var cell_count = 1; cell_count < cell_data.length; cell_count++) {
                table_data += '<td>' + cell_data[cell_count] + '</td>';
            }
            table_data += '</tr>';
        }
    }
    table_data += '</table>';
    console.log(table_data);
    $('#global_data').html(table_data);
}

