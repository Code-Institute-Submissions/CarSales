queue()
    .defer(d3.json, "/report/dashboard")
    .await(makeGraphs);

    function makeGraphs(error, chartOrders) {

        if (error) {
            console.error("makeGraphs error on receiving dataset:", error.statusText);
            throw error;
        }
        var parseDate = d3.time.format("%d/%m/%Y").parse;
        chartOrders.forEach(function(d){
            d.order_date = parseDate(d.order_date);
        });

        //Create a Crossfilter instance
        var ndx = crossfilter(chartOrders);

        var dateDim = ndx.dimension(function(d){
            return d.order_date;
        });
        var quantities = dateDim.group().reduceSum(function (d) {
		   return d.orderline;
		});
//        var stockDim = ndx.dimension(function(d){
//            return d.basket.stock.name;
//        });

        var ordersByDate = dateDim.group();

        //Define values (to be used in charts)
        var minDate = dateDim.bottom(1)[0].order_date;
        var maxDate = dateDim.top(1)[0].order_date;

        var timeChart = dc.lineChart("#chart-line-hitsperday");

        timeChart.width(540)
                 .height(405)
                 .dimension(dateDim)
                 .group(quantities, "Orders")
                 .renderArea(true)
                 .brushOn(false)
                 .x(d3.time.scale().domain([minDate, maxDate]))
                 .legend(dc.legend().x(450).y(10).itemHeight(13).gap(5))
                 .yAxisLabel("Items Sold Per Day");

        dc.renderAll();
    }