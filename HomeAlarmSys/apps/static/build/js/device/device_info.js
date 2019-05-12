$(function () {
    getAlarmInfo();
    getFireInfo();
    getSmokeInfo();
});

function getAlarmInfo(){
    $.ajax({
        url: "/device/alarm",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        success: function (r) {
            ''
        }
    })
}

function getFireInfo(){

}

function getSmokeInfo(){

}