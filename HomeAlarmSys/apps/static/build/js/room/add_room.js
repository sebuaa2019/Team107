$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    console.log(a);
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [ o[this.name] ];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};




var $addRoomForm = $("#add-room-form");

$(function () {

    $("#add-room-btn").click(function () {
        var name = $(this).attr('name');
        if (name ==='save') {
            $.ajax({
                    url: '/room/add/',
                    type: 'POST',
                    data: JSON.stringify($addRoomForm.serializeObject()),
                    contentType: 'application/json; charset=utf-8',
                    success:function (r) {
                        if (r === '200'){
                            closeModal();
                            $TableManager.n_success(r);
                            $TableManager.refreshTable('roomTable');
                        }
                        else $TableManager.n_danger(r)
                    }
                }
            );
        }
        if (name === 'update'){
            var $form = $addRoomForm.serializeObject();
            $form['id'] =  $("#roomTable").bootstrapTable("getSelections")[0].id;
            $.ajax({
                    url: '/room/update/',
                    type: 'POST',
                    referer:"/room/manage",
                    data: JSON.stringify($form),
                    contentType: 'application/json; charset=utf-8',
                    success:function (r) {
                        if (r === '200'){
                            closeModal();
                            $TableManager.n_success(r);
                            $TableManager.refreshTable('roomTable');
                        }
                        else $TableManager.n_danger(r)
                    }
                }
            );

        }

    });
});

function closeModal() {
    $('#add-room-btn').attr('name', 'save');
    $('#add-room-modal-title').html('添加房间');
    $TableManager.closeAndRestModal('room-add');

}


