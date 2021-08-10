window.onload = set_patient_details;

function set_patient_details() {
    const patient = JSON.parse(document.getElementById('patient').textContent);
    
    // set all fields to disabled mode
    document.getElementById('patient_name').value = patient['name'];
    document.getElementById('gender').value = patient['gender'];
    document.getElementById('p_contact').value = patient['p_mobile'];
    document.getElementById('s_contact').value = patient['s_mobile'];
    document.getElementById('status').value = patient['status'];
    document.getElementById('adhar').value = patient['adhar'];
    document.getElementById('dob').value = patient['dob'];
    document.getElementById('bed').value = patient['bed'];

    change_fields_mode(true);
}


function change_fields_mode(ack) {
    if (ack == false) {
        document.getElementById('edit-btn').style.display = "none";
        document.getElementById('update-btn').style.display = "block";
    } else if (ack=true) {
        document.getElementById('edit-btn').style.display = "block";
        document.getElementById('update-btn').style.display = "none";
    }
    document.getElementById('patient_name').disabled = ack;
    document.getElementById('patient_name').disabled = ack;
    document.getElementById('gender').disabled = ack;
    document.getElementById('p_contact').disabled = ack;
    document.getElementById('s_contact').disabled = ack;
    document.getElementById('status').disabled = ack;
    document.getElementById('adhar').disabled = ack;
    document.getElementById('dob').disabled = ack;
    document.getElementById('bed').disabled = ack;
}

function update_patient_details() {
    patient_name = document.getElementById('patient_name').value;
    gender = document.getElementById('gender').value;
    p_mobile = document.getElementById('p_contact').value;
    s_mobile = document.getElementById('s_contact').value;
    status = document.getElementById('status').value;
    adhar = document.getElementById('adhar').value;
    dob = document.getElementById('dob').value;
    bed = document.getElementById('bed').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    const patient = JSON.parse(document.getElementById('patient').textContent);

    $.ajax({
        type: 'POST',
        url: '/customer/update-patient-info/',
        data: {
            'name': patient_name,
            'gender': gender,
            'p_mobile': p_mobile,
            's_mobile': s_mobile,
            'adhar': adhar,
            'dob': dob,
            'status': status,
            'bed': bed,
            'slug': patient['slug'],
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            update = res['update'];
            if (update == true) {
                document.getElementById('adhar').classList.remove('is-invalid');
                document.querySelector('.alert-msg').style.display = "block";
                document.querySelector('.alert-msg').style.color = "green";
                document.querySelector('.alert-msg').innerText = "Patient info updated successfully."
                change_fields_mode(true);
                setTimeout(function() {
                    document.querySelector('.alert-msg').style.display = "none";
                }, 3000);
            } else {
                document.getElementById('adhar').classList.add('is-invalid');
                document.querySelector('.alert-msg').style.display = "block";
                document.querySelector('.alert-msg').style.color = "red";
                document.querySelector('.alert-msg').innerText = "Adhar number already exists. Please enter another one."
                setTimeout(function() {
                    document.querySelector('.alert-msg').style.display = "none";
                }, 3000);
            }
        }
    });
}
