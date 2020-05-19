Papa.parse("https://raw.githubusercontent.com/covid-projections/covid-data-public/master/data/covid-care-map/healthcare_capacity_data_state.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})


function displayHTMLTable(results) {
    var data = results.data;
    var colors = {"2": "rgb(230, 0, 169)", "3": "rgb(227, 139, 79)", "4": "rgb(132, 0, 168)"}

    var table_data = '<table class="table table-bordered table-sm table-striped table-dark">';
    for (var count = 0; count < data.length; count++) {
        var cell_data = Object.keys(data[count]).map(function(key){
            return data[count][key];
        });

        if (count === 0) { 
            table_data += '<thead class="thead-dark">' + 
                            '<th style="width: 25%;">' + 'State' + '<i class="fas fa-sort-up fa-1x"></i>' + '</th>' +
                            '<th style="width: 25%;">' + 'Staffed All Beds' + '</th>' +
                            '<th style="width: 25%;">' + 'Staffed ICU Beds' + '</th>' + 
                            '<th style="width: 25%;">' + 'Licensed All Beds' + '</th>' +
                          '</thead>';
        } else if (cell_data[1] === undefined) {
            continue;
        } else {
            table_data += '<tr>';
            for (var cell_count = 1; cell_count < 5; cell_count++) {
                if (cell_count !== 1) {
                    table_data += '<td style="color: ' + colors[cell_count.toString()] + ';">' + parseInt(cell_data[cell_count]) + '</td>';
                } else {
                    table_data += '<td>' + cell_data[cell_count] + '</td>';
                }
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
