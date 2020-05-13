Papa.parse("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})


function displayHTMLTable(results) {
    var data = results.data;
    var table_data = '<table class="table table-bordered table-sm">';

    for (var count = 0; count < data.length; count++) {
        var cell_data = Object.keys(data[count]).map(function(key){
            return data[count][key];
        });

        if (count === 0) { 
            table_data += '<thead class="thead-dark">' + 
                            '<th>' + 'State' + '</th>' +
                            '<th>' + 'County' + '</th>' +
                            '<th>' + 'Cases' + '</th>' +
                          '</thead>';
        } else if (cell_data[5] === "" || cell_data[0] === "" || cell_data[5] === "Unassigned" || cell_data[5].substring(0, 6) === "Out of") {
            continue;
        } else {
            console.log(cell_data);
            table_data += '<tr>';
            // Only display state, county, and cases
            for (var cell_count = 0; cell_count < cell_data.length; cell_count++) {
                if (cell_count === 6 || cell_count === 10 || cell_count === cell_data.length - 1) {
                    if (cell_count === 10) {
                        var county = cell_data[cell_count].split(',')[0];
                        table_data += '<td>' + county + '</td>';
                    } else {
                        table_data += '<td>' + cell_data[cell_count] + '</td>';
                    }
                }
            }
            table_data += '</tr>';
        }
    }
    table_data += '</table>';
    $('#county_data_table').html(table_data);
    
    
    // Sort data when table header cell clicked on
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
