Papa.parse("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})


function displayHTMLTable(results) {
    var data = results.data;
    var colors = {"2": "text-danger", "3": "text-success", "4": "text-warning"}

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
                            '<th style="width: 31%;">' + 'Country' + '<i class="fas fa-sort-up fa-1x"></i>' + '</th>' +
                            '<th style="width: 23%;">' + 'Confirmed' + '</th>' +
                            '<th style="width: 23%;">' + 'Recovered' + '</th>' + 
                            '<th style="width: 23%;">' + 'Deaths' + '</th>' +
                          '</thead>' +
                          '<tbody>';
        } else if (cell_data[0] !== d) {
            continue;
        } else {
            table_data += '<tr>';
            // Exclude data since we only want to show most recent data
            for (var cell_count = 1; cell_count < cell_data.length; cell_count++) {
                table_data += '<td class="' + colors[cell_count.toString()] +  '">' + cell_data[cell_count] + '</td>';
            }
            table_data += '</tr>';
        }
    }
    table_data += '</tbody></table>';
    $('#global_data_table').html(table_data);
    
    
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
