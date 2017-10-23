var pieChart, rowChart;

$.ajax({
    type: 'GET',
    url:'history_dashboard',
    success: function(data) {
        prepareCharts(data);
    },
    failure: function(response){
       console.log("Failure");
    }
});

function getScreenWidth(){
    return $('html').width();
};

var monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ],
    colours = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00',
        '#a65628', '#bc8f8f', '#8b4789', '#3a5fcd', '#607b8b', '#4a708b',
        '#fb6fb4', '#008b76', '#b82000', '#f9a114', '#00738', '#778217'
    ],
    parseDate = d3.time.format("%Y-%m-%d").parse;

function prepareCharts(salesData){
    var cf = crossfilter(salesData);

    preparePieChart(cf, 'make', '#makes_pie_chart');
    preparePieChart(cf, 'colour', '#colour_pie_chart');
    preparePieChart(cf, 'transmission', '#transmission_pie_chart');
    preparePieChart(cf, 'fuel_type', '#fuel_pie_chart');
    preparePieChart(cf, 'seats', '#seats_pie_chart');
    preparePieChart(cf, 'engine_size', '#engine_pie_chart');

    prepareRowChart(cf, 'model', '#models_row_chart');

    // Have had to remove the bar chart, as I can't seem to get the chart to render properly.
    //prepareBarChart(cf, 'order_date', '#sale_timeline');
    prepareDataTable(salesData, cf);

    prepareTotals(cf, '#total-sales');

    dc.renderAll();
};

function preparePieChart(cf, chartDimension, chartId){
    pieChart = dc.pieChart(chartId),
        dimension = cf.dimension(function(d){
            return d[chartDimension];
        }),
        group = dimension.group();

    pieChart
        .ordinalColors(colours)
        .width(860)
        .height(350)
        .radius(150)
        .legend(dc.legend().x(20).y(20).itemHeight(15).gap(5))
        .transitionDuration(1500)
        .cx(400)
        .dimension(dimension)
        .group(group);
};

function prepareRowChart(cf, chartDimension, chartId){
    rowChart = dc.rowChart(chartId),
        dimension = cf.dimension(function(d){
            return d[chartDimension];
        }),
        group = dimension.group();
    var width = $(window).width() > 900 ? 860 : 600;

    rowChart
        .ordinalColors(colours)
        .width(width)
        .height(500)
        .dimension(dimension)
        .elasticX(true)
        .group(group)
        .xAxis().ticks(6);
};

function prepareBarChart(cf, chartDimension, chartId){
    var barChart = dc.barChart(chartId),
        dimension = cf.dimension(function(d){
            return d[chartDimension];
        }),
        group = dimension.group(),
        minDate = dimension.bottom(1)[0].order_date,
        maxDate = dimension.top(1)[0].order_date;

    console.log("------------------------------------- Bar Chart -----------------------------------------");
    console.log(dimension.top(Infinity), "\n", minDate, "\n", maxDate, "\n", group.top(Infinity));
    console.log("-----------------------------------------------------------------------------------------");

    barChart
        .width(800)
        .height(200)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .elasticY(true)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .transitionDuration(500)
        .xAxisLabel("Sales By Month")
        .dimension(dimension)
        .group(group);
}

function prepareDataTable(data, cf){
    var datatable = dc.dataTable("#dc-data-table"),
        dimension = cf.dimension(function(d){
            return d['order_date'];
        });

    data.forEach(function(d){
            d.order_date = parseDate(d.order_date);
            d.order_date.setDate(1);
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

function prepareTotals(cf, chartId){
    var totalsField = dc.numberDisplay(chartId),
        all = cf.groupAll();

        console.log(all.value());

    totalsField
        .formatNumber(d3.format("d"))
        .valueAccessor(function(d){
            return d;
        })
        .group(all);
};

function redrawCharts(chartType, chart, chartId){
    switch(chartType){
        case 'pie':
            var chartWidth = $(chartId).width();
            pieRadius = chartWidth >= 860 ? 200 : chartWidth * 0.35;

            chart.width(chartWidth)
                .cx([chartWidth / 2])
                .radius(pieRadius)
                .redraw();

            break;
        case 'row':
            var width = $(window).width() > 900 ? 860 : 600;

            rowChart.width(width)
                .redraw();

            rowChart.render();
            rowChart.transitionDuration(750);

            break;
        default:
            console.log("No charts type found");
            break;
    }
};

$(window).resize(function() {
    redrawCharts('pie', pieChart, '#makes_pie_chart');
    redrawCharts('pie', pieChart, '#colour_pie_chart');
    redrawCharts('pie', pieChart, '#transmission_pie_chart');
    redrawCharts('pie', pieChart, '#fuel_pie_chart');
    redrawCharts('pie', pieChart, '#seats_pie_chart');
    redrawCharts('pie', pieChart, '#engine_pie_chart');

    redrawCharts('row', rowChart, '#models_row_chart');

    console.log($(window).width());
});