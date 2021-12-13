setInterval(function () {
    $.ajax('/updatec', {
        success: function (data) {
            option_01004.series[0].data = JSON.parse(data)[0];
            option_01004.xAxis[0].data = JSON.parse(data)[1];
            chart_01004.setOption(option_01004);
            option_01005.series[0].data = JSON.parse(data)[2];
            chart_01005.setOption(option_01005);
            option_01001.series[0].data = JSON.parse(data)[3];
            chart_01001.setOption(option_01001);

            //console.log('成功',data[0]);
        },
        complete: function () {
            //console.log('完成');
        },
        error: function () {
            //console.log('失败');
        }
    })
},
    600000
)