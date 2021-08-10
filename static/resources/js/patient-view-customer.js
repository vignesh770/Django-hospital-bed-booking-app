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
