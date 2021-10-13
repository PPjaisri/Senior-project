$(function () {
    $('#inForm').submit(function () {
        let data = $('#inForm').find('input[name="url"]').val();
        alert(data);
        // window.location.href = "new.html";
    });
});