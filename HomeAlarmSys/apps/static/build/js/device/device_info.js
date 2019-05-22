$(function () {

    loadControlDevice();
    getAlarmInfo();
    getFireInfo();

});

function getAlarmInfo(){

    $.ajax({
        url: "/device/alarm/",
        type: 'POST',
        data:{},
        contentType: 'application/json; charset=utf-8',
        success: function (r) {
            if (r['alarm_control'] === 1)
                $('#alarm-info').find('h3').html("正在正常工作");
            else {
                $('#alarm-info').find('h3').html("注意!报警装置已被关闭!");
            }
            if (r['alarm_control'] === 1 && r['alarm_info'] === 1){
                $('#alarm-info').find('p').html("发现入侵!");
            }
            else if (r['alarm_control'] === 1 && r['alarm_info'] === 0){
                $('#alarm-info').find('p').html("未发现入侵");
            }
            else{
                $('#alarm-info').find('p').html("");
            }
        }
    })
}

function getFireInfo(){

    $.ajax({
        url: "/device/fire/",
        type: 'POST',
        data:{},
        contentType: 'application/json; charset=utf-8',
        success: function (r) {
            var $fire = $('#fire-info');
            if (r['alarm_control'] === 1)
                $fire.find('h3').html("正在正常工作");
            else {
                $fire.find('h3').html("注意!报警装置已被关闭!");
            }
            if (r['alarm_control'] === 1 && r['fire_info'] === 1){
                $fire.find('p').html("疑似发生火灾!");
            }
            else if (r['alarm_control'] === 1 && r['fire_info'] === 0){
                $fire.find('p').html("正常");
            }
            else{
                $fire.find('p').html("");
            }
        }
    })

}



function loadControlDevice(){

    var setting = {
        url:'/device/controlDeviceList/',
        columns:[
            {
                field: 'id',
                title: '设备id',

            },{
                field: 'device_name',
                title: '设备名称'
            },{
                field: 'arg',
                title: '状态',
                formatter:function (value, row, index) {
                    if (value === 1){
                        return '<span class="badge badge-success" style="background-color:#97b72b">开</span>';
                    }
                    else{
                        return '<span class="badge badge-warning" style="background-color:#f98473">关</span>';
                    }
                }
            },{
                title:'操作',
                events:window.operateEvents,
                formatter: function () {
                    return '<a class="on-off" href="javascript:void(0)" onclick="onOff()"><i class="fa fa-power-off" </a>'
                }
            }
        ]
    };
    $TableManager.initTable('control-device-table', setting)

}

window.operateEvents = {
    'click .on-off':function (e, value, row, index){
        $.ajax({
            url:'/device/on_off/',
            type: 'GET',
            data: {"id":row.id},
            success: function (r) {
                $TableManager.refreshTable("control-device-table")
            }
        })
    }
};

function onOff(){
    $('#control-device-table').bootstrapTable({
        "onClickRow":function f(row, $element, field) {

        }
    })
}