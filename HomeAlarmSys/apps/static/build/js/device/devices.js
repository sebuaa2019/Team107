$(function () {
    var deviceTableForm = $("#device-table-form");
    var settings = {
        url : "/device/table/",
        pageSize: 10,
        // queryParams: function(params){
        //     return{
        //         pageNum:params.offset/params.limit+1,
        //     };
        // },
        columns:[{
            checkbox: true,
        }, {
            field:'id',
            title:'设备id'
        },{
            field:'device_name',
            title:'设备名称'
        },{
            field:'status',
            title:'状态',
            formatter: function (value, row, index) {
                if (value===1) return '<span class="badge badge-success" style="background-color:#97b72b">启用</span>';
                if (value===0) return '<span class="badge badge-warning">禁用</span>';
            }
        },{
            field:'arg_type',
            title:'参数类型',
            formatter: function (value, row, index) {
                if (value===1) return '<span class="badge badge-success" style="background-color:#97bc2d">布尔类型</span>';
                if (value===0) return '<span class="badge badge-success" style="background-color:#eb9589">数值型</span>';
            }
        },{
            field: 'arg',
            title:'参数值'

        }

        ]
    };
    $TableManager.initTable('deviceTable', settings);
});