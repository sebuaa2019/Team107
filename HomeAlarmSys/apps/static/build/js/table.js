var $TableManager = (function () {
    var bootstrapTable_default = {
        method : 'get',
        striped:true,
        cache:false,
        pagination:true,
        sortable:false,
        sidePagination:'client',
        pageNumber: 1,
        pageSize: 10,
        //pageList: [5, 10, 25, 50, 100],
        showColumns: false,
        minimumCountColumns:2,
        clickToSelect: true,
        uniqueId:"ID",
        cardView:false,
        smartDisplay:false,
    };
    function _initTable(id, settings){
        var params = $.extend({}, bootstrapTable_default, settings);
        if (typeof params.url === 'undefined'){
            throw '初始化表格失败';
        }
        if (typeof params.columns === 'undefined'){
            throw '初始化表格失败, 请配置columns';
        }
        $('#'+id).bootstrapTable(params);

    }

    function _refreshTable(id){
        $("#"+id).bootstrapTable('refresh');
    }

    function _notify(message, type) {
        $.notify({
            icon: "fa fa-check",
            title: "",
            message: message,
            url: ''
            }, {
            element: 'body',
            type: type,
            allow_dismiss: true,
            placement: {
                from: "top",
                align: "center"
            },
            offset: {
                x: 20,
                y: 20
            },
            spacing: 10,
            z_index: 3001,
            delay: 2500,
            timer: 1000,
            url_target: '_blank',
            mouse_over: false,
            animate: {
                enter: "animated fadeInDown",
                exit: "animated fadeOutUp"
            },
            template: '<div data-notify="container" class="alert alert-dismissible alert-{0} alert--notify" role="alert">' +
                '<span data-notify="icon"></span> ' +
                '<span data-notify="title">{1}</span> ' +
                '<span data-notify="message" style="font-weight: 600">{2}</span>' +
                '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0;"></div>' +
                '</div>' +
                '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>'
        });
    }


    function _closeAndRestModal(modalId) {
        var $modal = $("#" + modalId);
        $modal.modal("hide");
        //$modal.find(".btn-hide").attr("data-dismiss", "modal").trigger('click');
        $modal.find("form")[0].reset();
    }

    return {
        initTable: function(id, settings){
            _initTable(id, settings);
        },
        refreshTable:function (id) {
            _refreshTable(id);
        },
        n_default: function (message) {
            _notify(message, "inverse");
        },
        n_info: function (message) {
            _notify(message, "info");
        },
        n_success: function (message) {
            _notify(message, "success");
        },
        n_warning: function (message) {
            _notify(message, "warning");
        },
        n_danger: function (message) {
            _notify(message, "danger");
        },
        closeAndRestModal: function (modalId) {
            _closeAndRestModal(modalId);
        }

    }
})($);