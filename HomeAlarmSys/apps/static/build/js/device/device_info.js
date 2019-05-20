$(function () {
    loadControlDevice();
    getAlarmInfo();
    getFireInfo();
    getSmokeInfo();

});

function getAlarmInfo(){


    $.ajax({
        url: "/device/alarm/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        success: function (r) {

        }
    })
}

function getFireInfo(){

}

function getSmokeInfo(){

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