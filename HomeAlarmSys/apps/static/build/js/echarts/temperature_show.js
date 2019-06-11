var myChart = echarts.init(document.getElementById('tem_hum'));
var symbolSize = 5;
var option1 = {

    legend: {
        data: [
            "温度", '湿度'
        ],
    },
    xAxis: {
        min: 0,
        max: 10,
        type: 'value',
        axisLine: {onZero: false}
    },
    yAxis: {
        min: 0,
        max: 50,
        type: 'value',
        axisLine: {onZero: false}
    },
    series: [

        {
            name: '温度',
            id: 'a1',
            type: 'line',
            smooth: true,
            symbolSize: symbolSize,
            data: [[1, 24], [2, 26],[3, 25],[4, 24], [5, 26],[6, 25],[7, 24], [8, 26],[9, 25], [10, 23]],
        },
        {
            name: '湿度',
            id: 'a2',
            type: 'line',
            smooth: true,
            symbolSize: symbolSize,
            data: [[1, 18], [2, 26],[3, 30],[4, 22], [5, 22],[6, 23],[7, 21], [8, 25],[9, 21], [10, 21]],
        },
    ]
};
 myChart.setOption(option1, true);
