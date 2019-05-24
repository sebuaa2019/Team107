$(function () {

    var settings = {
        url : "/service/triTable/",
        pageSize: 10,

        columns:[{
            checkbox: true,
        }, {
            field:'id',
            title:'id'
        },{
            field:'name',
            title:'服务名称'
        }
        ]
    };
    $TableManager.initTable('triServiceTable', settings);
});


$(function () {

    var settings = {
        url : "/service/actTable/",
        pageSize: 10,

        columns:[{
            checkbox: true,
        }, {
            field:'id',
            title:'id'
        },{
            field:'name',
            title:'服务名称'
        }
        ]
    };
    $TableManager.initTable('actServiceTable', settings);
});