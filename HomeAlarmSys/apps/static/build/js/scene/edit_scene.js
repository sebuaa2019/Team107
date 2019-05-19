function updateScene(){
    var selected = $("#sceneTable").bootstrapTable("getSelections");
    var selected_length = selected.length;
    if (selected_length < 1){
        $TableManager.n_warning('请勾选需要修改的场景!');
        return;
    }
    if (selected_length > 1){
        $TableManager.n_warning('一次只能修改一个场景!');
        $TableManager.n_warning('一次只能修改一个场景!');
        return;
    }
    var sceneId = selected[0].id;
    $.ajax({
        url: '/scene/getScene/',
        data: JSON.stringify({"sceneId": sceneId}),
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        success: function (r) {
            var $form = $('#scene-add');
            $form.modal();
            var scene = r;
            $('#add-scene-modal-title').html('修改场景');
            $form.find("input[name='scene_name']").val(scene.scene_name);
            $form.find('#triggerSelect').val(scene.trigger['readserviceid']);
            $form.find('#tri-condition').val(scene.trigger['condition']);
            $form.find("input[name='arg']").val(scene.trigger['value']);
            $form.find('#actionSelect').val(scene.action['controlserviceid']);
            if (scene.action['value'] === true)
                $form.find('#action-val').val(1);
            else   $form.find('#action-val').val(0);

            var status = scene.status;
            if (status === 1) {
                $("#statusRadio1").prop("checked", true);
                $("#statusRadio1").val(1);
                $("#statusRadio2").val(0);
            } else {
                $("#statusRadio2").prop("checked", true);
                $("#statusRadio1").val(1);
                $("#statusRadio2").val(0);
            }
            $("#add-scene-btn").attr("name", "update");
            }
        });


}