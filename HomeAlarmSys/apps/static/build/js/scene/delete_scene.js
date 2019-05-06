function deleteScene(){
    var selected  = $('#sceneTable').bootstrapTable('getSelections');
    var selected_length = selected.length;
    if (selected_length === 0 ){
        $TableManager.n_warning("请勾选要删除的角色");
        return;
    }
    var ids = "";
    for (var i = 0; i < selected_length; i++){
        ids += selected[i].id;
        if (i!== (selected_length-1)) ids+=',';
    }



    $.ajax({
        url: '/scene/delete/',
        type: 'POST',
        data: JSON.stringify({"idString":ids}),
        success: function (r) {
            if (r=== '200'){
                $TableManager.n_success(r);
                $TableManager.refreshTable('sceneTable');
            }
            else{
                $TableManager.n_danger(r);
            }
        }
    })


}