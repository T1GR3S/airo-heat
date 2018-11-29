var $table_aps = $('#table_aps');

var mydata = (function () {
    var mydata = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': 'aps.json',
        'dataType': "json",
        'success': function (data) {
            mydata = data;
        }
    });
    return mydata;
})();

    
$(function () {
    $('#table_aps').bootstrapTable({
        data: mydata
    });
});
