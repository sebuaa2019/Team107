$(function () {

    var settings = {
        url : "/service/table/",
        pageSize: 10,

        columns:[{
            checkbox: true,
        }, {
            field:'id',
            title:'id'
        },{
            field:'name',
            title:'服务名称'
        },{
            field:'type',
            title:'类型'
        }
        ]
    };
    $TableManager.initTable('serviceTable', settings);
});