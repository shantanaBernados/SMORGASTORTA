$(document).ready(function(){
    document.getElementsByTagName("html")[0].style.visibility = "visible";
    $('input[type="text"],input[type="password"],input[type="email"]').prop('required', true);

    var setCSRFToken = function(xhr) {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            if (cookies[i].indexOf('csrftoken') == 0) {
                xhr.setRequestHeader('X-CSRFToken', cookies[i].split('=')[1]);
                break;
            }
        }
    }
    $('.helptext').remove();
    $('label').remove();
    $('#id_first_name').attr("placeholder", "First Name");
    $('#id_last_name').attr("placeholder", "Last Name");
    $('#id_email').attr("placeholder", "Email");
    $('#id_username').attr("placeholder", "Username");
    $('#id_password').attr("placeholder", "Password");
    $('#id_password1').attr("placeholder", "Password");
    $('#id_password2').attr("placeholder", "Re-type Password");

   $('#hwqForm').on('submit', function(e){
        // e.preventDefault();
        // $.post('assess', $(this).serialize(), function(data) {
        //     console.log(data);
        // });
   });
});