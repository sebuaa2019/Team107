$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    //console.log(a);
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




var $addSceneForm = $("#add-scene-form");
var $triggerSelect = $("#triggerSelect");
var $actionSelect = $("#actionSelect");

$(function () {
    initService();
    $("#add-scene-btn").click(function () {
        var name = $(this).attr('name');
        if (name ==='save') {
            $.ajax({
                    url: '/scene/add/',
                    type: 'POST',
                    data: JSON.stringify($addSceneForm.serializeObject()),
                    contentType: 'application/json; charset=utf-8',
                    success:function (r) {
                        if (r === '200'){
                            closeModal();
                            $TableManager.n_success(r);
                            $TableManager.refreshTable('sceneTable');
                        }
                        else $TableManager.n_danger(r)
                    }
                }
            );
        }
        if (name === 'update'){
            var $form = $addSceneForm.serializeObject();
            $form['id'] =  $("#sceneTable").bootstrapTable("getSelections")[0].id;
            $form['status'] =$addSceneForm.find("input[name='status']:checked").val();
            $.ajax({
                    url: '/scene/update/',
                    type: 'POST',
                    referer:"/scene/manage",
                    data: JSON.stringify($form),
                    contentType: 'application/json; charset=utf-8',
                    success:function (r) {
                        if (r === '200'){
                            closeModal();
                            $TableManager.n_success(r);
                            $TableManager.refreshTable('sceneTable');
                        }
                        else{
                            closeModal();
                            $TableManager.refreshTable('sceneTable');
                            $TableManager.n_danger(r)
                        }
                    }
                }
            );

        }

    });
});

function closeModal() {
    $('#add-scene-btn').attr('name', 'save');
    $('#add-scene-modal-title').html('添加场景');
    $TableManager.closeAndRestModal('scene-add');

}

function initService(){
    $.ajax({
        url:'/scene/serviceList/',
        type:'POST',
        contentType:'application/json; utf-8',
        success:function (r) {
            var readServices = r['readService'];
            var controlServices = r['controlService'];

            var option = "";
            for (var i = 0; i < readServices.length; i++){
                option += "<option value='" +readServices[i].id+"'>"
                    +readServices[i].name+"</option>"
            }
            $triggerSelect.html("").append(option);

            option = "";
            for (i = 0; i < controlServices.length; i++){
                option += "<option value='" +controlServices[i].id+"'>"
                    +controlServices[i].name+"</option>"
            }
            $actionSelect.html("").append(option);

        }
    });
}



