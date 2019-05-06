function updateRoom(){
    var selected = $("#roomTable").bootstrapTable("getSelections");
    var selected_length = selected.length;
    if (selected_length < 1){
        $TableManager.n_warning('请勾选需要修改的房间!');
        return;
    }
    if (selected_length > 1){
        $TableManager.n_warning('一次只能修改一个房间!');
        $TableManager.n_warning('一次只能修改一个房间!');
        return;
    }
    var roomId = selected[0].id;
    $.ajax({
        url: '/room/getRoom/',
        data: JSON.stringify({"roomId": roomId}),
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        success: function (r) {
            var $form = $('#room-add');
            $form.modal();
            var room = r;
            $('#add-room-modal-title').html('修改房间');
            $form.find("input[name='room_name']").val(room.room_name);
            $("#add-room-btn").attr("name", "update");
            }
        });


}