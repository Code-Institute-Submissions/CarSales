$.ajax({
    type: 'GET',
    url:'reporting_bar_chart',
    success: function(data) {
        console.log(data);

        prepareChart(data);
    },
    failure: function(response){
       console.log("Failure");
    }
});

var monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function prepareChart(salesData){
    var salesLineChart = dc.lineChart('#sales_line_chart');
    var salesPieChart = dc.pieChart('#sales_pie_chart');

    var ndx = crossfilter(salesData);
    var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S").parse;

    salesData.forEach(function(d){
        d.order_date = parseDate(d.order_date);
        d.month = d.order_date.getMonth();
        d.order_year = d.order_date.getFullYear();
        d.make=  d.make;
        d.model = d.model;
        d.year = d.year;
        d.fuel_type = d.fuel_type;
        d.engine_size = d.engine_size;
        d.seats = d.seats;
        d.colour = d.colour;
        d.transmission = d.transmission,
        d.price = d.price;
        d.mileage = d.mileage;
    });

    var dateDimension = ndx.dimension(function(d){
        return d.order_date.getDate();
    });

    var carYearDimension = dateDimension.group().reduceSum(function(d){
        return d.year;
    });

    var makeDimension = dateDimension.group().reduceSum(function(d){
        return d.make;
    });

    var modelDimension = dateDimension.group().reduceSum(function(d){
        return d.model;
    });

    var colourDimension = dateDimension.group().reduceSum(function(d){
        return d.colour;
    });

    var priceDimension = dateDimension.group().reduceSum(function(d){
        return +d.price;
    })

    var minDate = dateDimension.bottom(1)[0].order_date;
    var maxDate = dateDimension.top(1)[0].order_date;

    console.log(makeDimension);

    salesLineChart.width(540)
					 .height(405)
					 .dimension(dateDimension)
					 .group(carYearDimension, "Year")
					 .stack(makeDimension, "Make")
					 .renderArea(true)
					 .brushOn(false)
					 .x(d3.time.scale().domain([minDate, maxDate]).nice())
					 .legend(dc.legend().x(450).y(10).itemHeight(13).gap(5))
					 .yAxisLabel("Sold Per Month")
					 .xAxis();


	var yearDimension = ndx.dimension(function(d){
	    return +d.order_year;
	});

	console.log(yearDimension);


    salesPieChart.width(300)
                .height(300)
                .slicesCap(5)
                .innerRadius(100)
                .dimension(dateDimension)
                .group(carYearDimension);

    var datatable = dc.dataTable("#dc-data-table");
    datatable.dimension(dateDimension)
            .group(function (d) {
                return monthNames[d.month];
            })// create the columns dynamically
            .columns([function (d) {
               return d.order_date.getDate() + "/" + (d.order_date.getMonth() + 1) + "/" + d.order_date.getFullYear();
            },
            function (d) {
               return d.make;
            },
            function (d) {
               return d.model;
            },
            function (d) {
               return d.year;
            },
            function (d) {
               return parseFloat(d.price).toFixed(2);
            },
            function (d) {
               return d.engine_size;
            },
            function (d) {
               return d.seats;
            },
            function (d) {
               return d.colour;
            },
            function (d) {
               return d.fuel_type;
            },
            function(d){
            return d.mileage}
        ]);

    // Now tell dc to render the chart/s
    dc.renderAll();
};
