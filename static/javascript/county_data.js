Papa.parse("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})


function displayHTMLTable(results) {
    var data = results.data;
    var table_data = '<table class="table table-bordered table-sm table-striped table-dark">';

    for (var count = 0; count < data.length; count++) {
        var cell_data = Object.keys(data[count]).map(function(key){
            return data[count][key];
        });

        if (count === 0) { 
            table_data += '<thead class="thead-dark">' + 
                            '<th style="width: 40%;">' + 'State' + '<i class="fas fa-sort-up fa-1x"></i>' + '</th>' +
                            '<th style="width: 40%;">' + 'County' + '</th>' +
                            '<th style="width: 20%;">' + 'Cases' + '</th>' +
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
                    } else if (cell_count === 6) {
                        table_data += '<td>' + cell_data[cell_count] + '</td>';
                    } else {
                        table_data += '<td class="text-danger">' + cell_data[cell_count] + '</td>';
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

        // If ascending, show up arrow icon. Else, show down arrow icon.
        if (this.asc) {
            $('.fa-sort-down').remove();
            $('.fa-sort-up').remove();
            $(this).append('<i class="fas fa-sort-up fa-1x"></i>');
        } else {
            $('.fa-sort-up').remove();
            $('.fa-sort-down').remove();
            $(this).append('<i class="fas fa-sort-down fa-1x"></i>');
        }

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
