$(function () {
    var sceneTableForm = $("#scene-table-form");
    var settings = {
        url : "/scene/table/",
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
            title:'场景id'
        },{
            field:'scene_name',
            title:'场景名称'
        },{
            field:'status',
            title:'状态',
            formatter: function (value, row, index) {
                if (value===1) return '<span class="badge badge-success" style="background-color:green">启用</span>';
                if (value===0) return '<span class="badge badge-warning">禁用</span>';
            }
        }
        ]
    };
    $TableManager.initTable('sceneTable', settings);
});