'use strict'

{
    window.onload = function(){
        console.log("Load OK");
        //テストデータ1
        var chartData = [];
        var chartLabels = [];
        chartLabels["labels"] = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
        var dataSets = [];
        var data = [];
        data["label"] = "友達登録数";
        data["data"] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120];
        dataSets["datasets"] = [];
        dataSets["datasets"].push(data);

        chartData.push(chartLabels);
        chartData.push(dataSets);
        //テストデータ2
        var chartData2 = [];
        var chartLabels2 = [];
        chartLabels2["labels"] = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
        var dataSets2 = [];
        var data2 = [];
        data2["label"] = "友達登録数";
        data2["data"] = [120, 110, 100, 90, 80, 70, 60, 50 ,40, 30, 20,10];
        dataSets2["datasets"] = [];
        dataSets2["datasets"].push(data2);

        chartData2.push(chartLabels2);
        chartData2.push(dataSets2);
        //テストデータ終了

        createChart("myChart1", "line", chartData[0].labels, chartData[1].datasets);
        createChart("myChart2", "line", chartData2[0].labels, chartData2[1].datasets);
    }

 
    //基本色
    var defColor = ["#3451A4", "#88CCEE", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255", "#AA4499", "#DDDDDD"];


    //関数の作成
    function createChart(cahartID, chart_type, chartLabels, chartDataSets) {
        var retChart;
        var ctx = document.getElementById(cahartID);
        console.log(chartDataSets);
        retChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: createData(chart_type, chartDataSets, defColor)
            },
            options: createChartOption(chartDataSets),
        });

        return retChart;
    }

    var createData = function (chartType, chartData, defColor) {
        var returnDataSets = [];
        for (var itemIndex = 0; itemIndex < chartData.length; itemIndex++) {
            console.log(chartData[itemIndex].data);
            returnDataSets.push(createDataSet(chartType, chartData[itemIndex].label, chartData[itemIndex].data, defColor[itemIndex]))
        }

        return returnDataSets;
    }

    var createDataSet = function (chartType, dataLabel, chartData, color) {
        var retData = {
            type: chartType,
            label: dataLabel,
            backgroundColor: color,
            data: chartData,
            borderColor: color,
            lineTension: 0,
            fill: false,
            borderWidth: 3,
            datalabels: {
                tooltip: {
                    enabled: false
                },
                formatter: (value, ctx) => {
                    return value + '%';
                },
            }
        }

        return retData;
    }

    var createChartOption = function (ChartDataItems) {
        var temp_ChartDataItems = ChartDataItems["ChartOption"];
        var complexChartOption = {
            responsive: true,
            scales: {
                "yAxis-left": {
                    id: 'yAxis-left',
                    type: "linear",
                    display: true,
                    position: "left",
                    ticks: {
                        beginAtZero: true,//0からスタート
                        stepSize: 10,
                        callback: function (label, index, labels) {
                            return label;
                        }
                    },
                    title: {
                        display: true,
                        text: "左軸タイトル★今後修正必要"
                    },
                },
                "yAxis-right": {
                    id: "yAxis-right",
                    type: 'linear',
                    display: true,
                    position: 'right',
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: {
                        beginAtZero: true,//0からスタート
                        stepSize: 20,
                        callback: function (label, index, labels) {
                            return label;
                        }
                    },
                    title: {
                        display: true,
                        text: "右軸タイトル★今後修正必要"
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                },
            },
        };

        return complexChartOption;
    }
}