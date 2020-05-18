Papa.parse("https://raw.githubusercontent.com/covid-projections/covid-data-public/master/data/covid-care-map/healthcare_capacity_data_state.csv", {
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
                            '<th>' + 'State' + '<i class="fas fa-sort-up fa-1x"></i>' + '</th>' +
                            '<th>' + 'Staffed All Beds' + '</th>' +
                            '<th>' + 'Staffed ICU Beds' + '</th>' + 
                            '<th>' + 'Licensed All Beds' + '</th>' +
                          '</thead>';
        } else if (cell_data[1] === undefined) {
            continue;
        } else {
            table_data += '<tr>';
            for (var cell_count = 1; cell_count < 5; cell_count++) {
                table_data += '<td>' + cell_data[cell_count] + '</td>';
            }
            table_data += '</tr>';
        }
    }
    table_data += '</table>';
    $('#capacity_data_table').html(table_data);
    
    
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
