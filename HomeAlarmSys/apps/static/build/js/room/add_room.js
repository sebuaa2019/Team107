
var $addRoomForm = $("#add-room-form");

$(function () {

    $("#add-room-btn").click(function () {
        $.ajax({
            url: "/room/add/",
            type: "POST",
            data: JSON.stringify($addRoomForm.serializeArray()),
            contentType: "application/json; charset=utf-8"
        })
    });
});