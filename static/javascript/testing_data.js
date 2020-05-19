Papa.parse("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-latest-data-source-details.csv", {
    download: true,
    header: true,
	complete: displayHTMLTable
})


function displayHTMLTable(results) {
    var data = results.data;
    var table_data = '<table class="table table-bordered table-sm table-striped table-dark">';
    var colors = {"7": "rgb(10, 150, 41)", "8": "rgb(37, 167, 247)", "9": "rgb(23, 200, 87)", "10": "rgb(245, 141, 66)"}
    
    for (var count = 0; count < data.length; count++) {
        var cell_data = Object.keys(data[count]).map(function(key){
            return data[count][key];
        });

        if (count === 0) { 
            /*
            table_data += '<thead class="thead-dark" style="border-color: white;">' + 
                            '<th style="width: 20%;">' + 'Country' + '<i class="fas fa-sort-up fa-1x"></i>' + '</th>' +
                            '<th style="width: 10%;">' + 'Date' + '</th>' +
                            '<th style="width: 20%;">' + 'Source Label' + '</th>' +
                            '<th style="width: 10%;">' + 'Total' + '</th>' + 
                            '<th style="width: 15%;">' + 'Total per Thousand' + '</th>' +
                            '<th style="width: 10%;">' + 'Daily Change' + '</th>' +
                            '<th style="width: 15%;">' + 'Daily Change per Thousand' + '</th>' +
                          '</thead>';
            */
            table_data += '<thead class="thead-dark" style="border-color: white;">' + 
                            '<th id="c" style="width: 30%;">' + 'Country' + '<i class="fas fa-sort-up fa-1x"></i>' + '</th>' +
                            '<th id="t" style="width: 15%;">' + 'Total' + '</th>' + 
                            '<th id="tp" style="width: 20%;">' + 'Total per 1000' + '</th>' +
                            '<th id="dc" style="width: 15%;">' + 'Daily Change' + '</th>' +
                            '<th id="dcp" style="width: 20%;">' + 'Daily Change per 1000' + '</th>' +
                          '</thead>';
        } else if (cell_data[0] === "") {
            continue;
        } 
        else {
            table_data += '<tr>';
            // Data we want is in this range
            for (var cell_count = 1; cell_count < 11; cell_count++) {
                /*if (cell_count === 3 || cell_count === 5 || cell_count === 6) {
                    continue
                } */
                if (cell_count === 2 || cell_count === 3 || cell_count === 4 || cell_count === 5 || cell_count === 6) {
                    continue
                }
                table_data += '<td style="color: ' + colors[cell_count.toString()] + ';">' + cell_data[cell_count] + '</td>';
            }
            table_data += '</tr>';
        }
    }
    table_data += '</table>';
    $('#testing_data_table').html(table_data);
    
    
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
