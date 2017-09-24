$.ajax({
    type: 'GET',
    url:'reporting_bar_chart',
    success: function(data) {
        console.log(data);

        prepareCharts(data);
    },
    failure: function(response){
       console.log("Failure");
    }
});

var monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function prepareCharts(salesData){

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
        return d.order_date;
    });

     var dateDimensionTwo = ndx.dimension(function(d){
        return d.order_date;
    });

    var makeDimension = ndx.dimension(function(d){
        return d.make;
    });
    var makeDimensionTwo = ndx.dimension(function(d){
        return d.make;
    });

    var modelDimension = ndx.dimension(function(d){
        return d.model;
    });

    var modelDimensionTwo = ndx.dimension(function(d){
        return d.model;
    });

    // Calculations
    var makeGroup = makeDimension.group();
    var makeGroupTwo = makeDimensionTwo.group()
    var modelGroup = modelDimension.group();
    var modelGroupTwo = modelDimension.group();

    var modelGroupThree = modelDimension.group();

    var minDate = dateDimension.bottom(1)[0].order_date;
    var maxDate = dateDimension.top(1)[0].order_date;

    prepareRowChart(modelDimension, modelGroup, '#sales_row_chart');
    preparePieChart(makeDimensionTwo, makeGroup, '#makes_pie_chart');
    preparePieChart(modelDimensionTwo, modelGroupTwo, '#models_pie_chart');

    prepareDataTable(dateDimension);

    dc.renderAll();
};

function preparePieChart(dimension, group, chartId){
    var makesPieChart = dc.pieChart(chartId);

    makesPieChart
    .ordinalColors(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00', '#a65628'])
        .width(300)
		.height(300)
        .radius(100)
        .innerRadius(50)
        .transitionDuration(1500)
        .dimension(dimension)
        .group(group);
};

function prepareRowChart(dimension, group, chartId){
    var salesRowChart = dc.rowChart(chartId);

    salesRowChart
    .ordinalColors(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00', '#a65628'])
        .width(540)
		.height(405)
		.dimension(dimension)
		.group(group)
		.xAxis().ticks(6);
};

function prepareLineChart(dimension, group, stack, minDate, maxDate, chartId){
    var salesLineChart = dc.lineChart(chartId);

    salesLineChart.width(0)
                 .height(0)
                 .dimension(dimension)
                 .group(group, "makes")
                 .stack(stack, "models")
                 .renderArea(true)
                 .brushOn(false)
                 .x(d3.time.scale().domain([minDate, maxDate]))
                 .legend(dc.legend().x(450).y(10).itemHeight(13).gap(5))
                 .yAxisLabel("Sales Per Day");

};

function prepareDataTable(dimension){
    var datatable = dc.dataTable("#dc-data-table");
    datatable
        .dimension(dimension)
        .group(function (d) {
            return monthNames[d.month];
        })
        .order(function (d) {
            return d3.descending(d.month);
        })
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
};
