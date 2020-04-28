Papa.parse("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})


function displayHTMLTable(results) {
    var data = results.data;

    i = data.length - 1;
    if (data[i]["Date"] === "") i -= 1;
    var row = data[i];
    d = row["Date"];

    var table_data = '<table class="table table-bordered table-sm">';
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
            // Exclude data since we only want to show most recent data
            for (var cell_count = 1; cell_count < cell_data.length; cell_count++) {
                table_data += '<td>' + cell_data[cell_count] + '</td>';
            }
            table_data += '</tr>';
        }
    }
    table_data += '</table>';
    $('#global_data_table').html(table_data);
    
    
    $('th').click(function() {
        if (this.asc === undefined) {
            this.asc = true;
        }
        var table = $(this).parents('table').eq(0)
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
        this.asc = !this.asc
        if (!this.asc){
            rows = rows.reverse()
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i])
        }
    })
    function comparer(index) {
        return function(a, b) {
            var valA = getCellValue(a, index), valB = getCellValue(b, index)
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
        }
    }
    function getCellValue(row, index){ 
        return $(row).children('td').eq(index).text() 
    }
    
}
