

function updateDevice(){
    var selected = $("#deviceTable").bootstrapTable("getSelections");
    var selected_length = selected.length;
    if (selected_length < 1){
        $TableManager.n_warning('请勾选需要修改的设备!');
        return;
    }
    if (selected_length > 1){
        $TableManager.n_warning('一次只能修改一个设备!');
        $TableManager.n_warning('一次只能修改一个设备!');
        return;
    }
    var deviceId = selected[0].id;
    $.ajax({
        url: '/device/getDevice/',
        data: JSON.stringify({"deviceId": deviceId}),
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        success: function (r) {
            var $form = $('#device-add');
            $form.modal();
            var device = r;
            $('#add-device-modal-title').html('修改设备');
            $form.find("input[name='device_name']").val(device.device_name);
            $form.find("input[name='id']").val(device.id);
            $("#roomSelect").val(device.room_id);
            console.log(device.room_id);
            if (device.room_id == ""){
                $("#roomSelect").val(roomList[0].id);
            }
            var status = device.status;
            if (status === 1) {
                $("#statusRadio1").prop("checked", true);
                $("#statusRadio1").val(1);
                $("#statusRadio2").val(0);
            } else {
                $("#statusRadio2").prop("checked", true);
                $("#statusRadio1").val(1);
                $("#statusRadio2").val(0);
            }
            $("#add-device-btn").attr("name", "update");
            }
        });


}