document.getElementById('login-btn').addEventListener('click', login);

function login() {
    var username = document.getElementById('user_name').value;
    var password = document.getElementById('password').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    $.ajax({
        type: 'POST',
        url: '/hospital/login-hospital-authority/',
        data: {
            'username': username,
            'password': password,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            var login_status = false;
            login_status = res['login'];
            if(login_status == true) {
                var url = '/hospital/authority-dashboard';
                document.location.href = url;
            } else {
                document.getElementById('error-msg').innerHTML = res['error'];
            }
        }
    });

}

