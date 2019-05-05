$(function () {
    var roomTableForm = $("#room-table-form");
    var settings = {
        url : "/room/table/",
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
            title:'房间id'
        },{
            field:'room_name',
            title:'房间名称'
        }
        ]
    };
    $TableManager.initTable('roomTable', settings);
});