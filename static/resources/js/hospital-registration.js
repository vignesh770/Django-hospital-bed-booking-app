document.getElementById('reg-btn').addEventListener('click', register);

function register() {
    var hospital_name = document.getElementById('hospital_name').value;
    var hospital_id = document.getElementById('hospital_id').value;
    var state = document.getElementById('state').value;
    var city = document.getElementById('city').value;
    var address = document.getElementById('address').value;
    var hospital_type = document.getElementById('hospital_type').value;
    var email = document.getElementById('email').value;
    var help_line = document.getElementById('help_line').value;
    var username = document.getElementById('user_name').value;
    var password = document.getElementById('password').value;
    var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");

    var ack = false;

    if (!hospital_name) {
        document.getElementById('hospital_name').classList.add('is-invalid');
        document.getElementById('hospital_name_err_id').innerHTML="This field is required";
        ack = false;
    } else {
        document.getElementById('hospital_name').classList.remove('is-invalid');
        document.getElementById('hospital_name_err_id').innerHTML="";
        ack = true;
    }

    if (!address) {
        document.getElementById('address').classList.add('is-invalid');
        document.getElementById('hospital_address_err_id').innerHTML="This field is required";
        ack = false;
    } else {
        document.getElementById('address').classList.remove('is-invalid');
        document.getElementById('hospital_address_err_id').innerHTML="";
        ack = true;
    }

    if (!hospital_id) {
        document.getElementById('hospital_id').classList.add('is-invalid');
        document.getElementById('hospital_id_err_id').innerHTML="This field is required";
        ack = false;
    } else {
        document.getElementById('hospital_id').classList.remove('is-invalid');
        document.getElementById('hospital_id_err_id').innerHTML="";
        ack = true;
    }

    if (!state) {        
        document.getElementById('state').classList.add('is-invalid');
        document.getElementById('state_err_id').innerHTML="Select your state";
        ack = false;
    } else {
        document.getElementById('state').classList.remove('is-invalid');
        document.getElementById('state_err_id').innerHTML="";
        ack = true;
    }

    if (!city) {        
        document.getElementById('city').classList.add('is-invalid');
        document.getElementById('city_err_id').innerHTML="Select your city";
        ack = false;
    } else {
        document.getElementById('city').classList.remove('is-invalid');
        document.getElementById('city_err_id').innerHTML="";
        ack = true;
    }

    if (!hospital_type) {
        document.getElementById('hospital_type').classList.add('is-invalid');
        document.getElementById('hospital_type_err_id').innerHTML="Select your hospital type";
        ack = false;
    } else {
        document.getElementById('hospital_type').classList.remove('is-invalid');
        document.getElementById('hospital_type_err_id').innerHTML="";
        ack = true;
    }

    if (!email) {
        document.getElementById('email').classList.add('is-invalid');
        document.getElementById('email_err_id').innerHTML="Check your email id";
        ack = false;
    } else {
        document.getElementById('email').classList.remove('is-invalid');
        document.getElementById('email_err_id').innerHTML="";
        ack = true;
    }
    
    if (!username) {
        document.getElementById('user_name').classList.add('is-invalid');
        document.getElementById('user_name_err_id').innerHTML="Enter your user name";
        ack = false;
    } else {
        document.getElementById('user_name').classList.remove('is-invalid');
        document.getElementById('user_name_err_id').innerHTML="";
        ack = true;
    }

    if (!help_line) {
        document.getElementById('help_line').classList.add('is-invalid');
        document.getElementById('help_line_err_id').innerHTML="This field is required";
        ack = false;
    } else {
        if(!help_line.match(/^\d{10}$/)) {
            document.getElementById('help_line').classList.add('is-invalid');
            document.getElementById('help_line_err_id').innerHTML="Check your number";
            ack = false;
        } else {
            document.getElementById('help_line').classList.remove('is-invalid');
            document.getElementById('help_line_err_id').innerHTML="";
            ack = true;
        }
    }
    
    if (!password) {
        document.getElementById('password').classList.add('is-invalid');
        document.getElementById('password_err_id').innerHTML="Enter your password";
        ack = false;
    } else {
        if(!password.match(strongRegex)) {
            ack = false;
            console.log(password);
            alert("Password must contain the following:\nA lowercase letter\nA capital(uppercase) letter\nA number\nMinimum 8 characters");
        }
    }
    
    
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    if (ack == true) {
        $.ajax({
            type: 'POST',
            url: '/hospital/register-new-hospital/',
            data: {
                'name': hospital_name,
                'hospital_id': hospital_id,
                'state': state,
                'city': city,
                'address': address,
                'hospital_type': hospital_type,
                'email': email,
                'help_line': help_line,
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
                    document.getElementById('error-msg').innerHTML = res['username'];
                }
            }
        });
    }
}


