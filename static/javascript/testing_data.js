Papa.parse("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-latest-data-source-details.csv", {
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
            table_data += '<thead class="thead-dark" style="border-color: white;">' + 
                            '<th style="width: 20%;">' + 'Country' + '</th>' +
                            '<th style="width: 10%;">' + 'Date' + '</th>' +
                            '<th style="width: 20%;">' + 'Source Label' + '</th>' +
                            '<th style="width: 10%;">' + 'Cumulative Total' + '</th>' + 
                            '<th style="width: 15%;">' + 'Daily Change in Cumulative People' + '</th>' +
                            '<th style="width: 10%;">' + 'Cumulative total per thousand' + '</th>' +
                            '<th style="width: 15%;">' + 'Daily change in cumulative total per thousand' + '</th>' +
                          '</thead>';
        } else if (cell_data[0] === "") {
            continue;
        } 
        else {
            table_data += '<tr>';
            // Data we want is in this range
            for (var cell_count = 0; cell_count < 9; cell_count++) {
                if (cell_count === 2 || cell_count === 4) {
                    continue
                } 
                table_data += '<td>' + cell_data[cell_count] + '</td>';
            }
            table_data += '</tr>';
        }
    }
    table_data += '</table>';
    $('#testing_data').html(table_data);
    
    
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
