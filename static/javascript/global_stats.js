$(document).ready(function(){
    Papa.parse("https://raw.githubusercontent.com/datasets/covid-19/master/data/worldwide-aggregated.csv", {
            download: true,
            header: true,
            complete: getStats
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

    function getStats(results) {
        // create a date object using Date constructor 
        //var dateObj = new Date(); 
        // subtract one day from current time                           
        //dateObj.setDate(dateObj.getDate() - 1);
        var date = formatDate();
        //var table = "<table class='table table-bordered table-striped'>";
        var data = results.data;
        var cases = 0;
        var deaths = 0;
        var recoveries = 0;

        
        for (i = 0; i < data.length; i++){
            //table = "<tr>";
            var row = data[i];
            d = row["Date"];
            console.log(row);
            if (d === date) {
                cases = parseInt(row["Confirmed"]);
                deaths = parseInt(row["Deaths"]);
                recoveries = parseInt(row["Recovered"]);
            }
            
            /*
            var cells = row.join(",").split(",");
            
            for (j = 0; j < cells.length; j++){
                table += "<td>";
                table += cells[j];
                table += "</th>";
            }
            table += "</tr>";
            */
        }
        let casesString = "<p class='text-danger'>" + cases + "</p>";
        let deathString = "<p class='text-dark'>" + deaths + "</p>";
        let recoveriesString = "<p class='text-success'>" + recoveries + "</p>";
        //console.log(deathString);
        $("#cases").html(casesString);
        $("#deaths").html(deathString);
        $("#recoveries").html(recoveriesString);
    }
});