$(function () {
    $('#textForm').submit(function () {
        let data = $('#textForm').find('input[name="content"]').val();
        alert(data);
    });
});