setInterval(function () {
    $.ajax('/updatew', {
        success: function (data) {
            option_02001.series[0].data = JSON.parse(data)[0];
            chart_02001.setOption(option_02001);
            option_02002.series[0].data = JSON.parse(data)[1];
            chart_02002.setOption(option_02002);

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