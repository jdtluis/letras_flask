var containers = document.getElementsByClassName('chart');

for (var i = 0; i < containers.length; i++) {
// Data retrieved https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature
Highcharts.chart(containers[i], {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Curva de tasas'
    },
    subtitle: {
        text: containers[i].id
    },
    xAxis: {
            title: {
            text: 'Duration'
            }
        //categories: series[containers[i].id][2]
        //['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        //accessibility: {description: 'Months of the year'}
    },
    yAxis: {
        title: {
            text: 'TIR'
        },
        labels: {
        formatter: function() {
          return Highcharts.numberFormat(this.value*100, 1) + '%'
        }
        }
    },

        tooltip: {
      formatter: function() {
        return '<b>' + this.series.name + '</b>: ' + Highcharts.numberFormat(this.y*100, 2) + ' %   ' + '<b>' + 'DM' + '</b>:' + Highcharts.numberFormat(this.x, 1);
      }
    },

    plotOptions: {
        spline: {
            marker: {
                radius: 4,
                lineColor: '#666666',
                lineWidth: 1
            }
        }
    },
    series: [{
        name: 'TIR',
        marker: {
            symbol: 'circle'
        },
        data: series[containers[i].id][0]

    }, {
        name: 'Spline TIR Fit',
        marker: {
            symbol: 'diamond'
        },
        data: series[containers[i].id][1]
    }]
})
};
