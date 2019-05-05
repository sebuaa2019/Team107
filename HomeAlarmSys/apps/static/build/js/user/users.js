$(function () {
    var userTableForm = $("#user-table-form");
    var settings = {
        url : "/user/table",
        pageSize: 10,
        // queryParams: function(params){
        //     return{
        //         pageNum:params.offset/params.limit+1,
        //     };
        // },
        columns:[{
            checkbox: true,
        }, {
            field:'name',
            title:'用户名'
        },{
            field:'email',
            title:'邮箱'
        },{
            field:'phone',
            title:'手机'
        }
        ]
    };
    $TableManager.initTable('userTable', settings);
});