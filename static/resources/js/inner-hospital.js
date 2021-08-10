
window.onload = initAll;

function initAll() {
    get_bed_etails();
}


function get_bed_etails() {

    document.getElementById('alert').style.display = "none";
    document.getElementById('red-alert').style.display = "none";

    var hospital_slug = JSON.parse(document.getElementById('hospital_slug').textContent);
    var url = "/hospital/bed-details/" + hospital_slug;

    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        
        success: function (res) {
            document.getElementById('available-word-bed').innerText = res['available_word_bed'] - res['waiting_word_bed'];
            document.getElementById('waiting-word-bed').innerText = res['waiting_word_bed'];

            document.getElementById('available-icu-bed').innerText = res['available_icu_bed'] - res['waiting_icu_bed'];
            document.getElementById('waiting-icu-bed').innerText = res['waiting_icu_bed'];

            disable_or_enable_bed_type(res);
        }
    });
}

function disable_or_enable_bed_type(res) {
    var word_available = res['available_word_bed'] - res['waiting_word_bed'];
    var icu_availbale = res['available_icu_bed'] - res['waiting_icu_bed'];

    if (word_available < 1) {
        document.getElementById('bed').value = 'icu';
        document.getElementById('bed').disabled = true;
    } 

    if (icu_availbale < 1) {
        document.getElementById('bed').value = 'word';
        document.getElementById('bed').disabled = true;
    }

    if (icu_availbale < 1 && word_available < 1) {
        document.getElementById('open-model-btn').disabled = true;
    }

}


function add_patient() {
    var hospital = document.getElementById('hospital-name').value;
    var name = document.getElementById('patient-name').value;
    var gender = document.getElementById('gender').value;
    var p_mobile = document.getElementById('p_contact').value;
    var s_mobile = document.getElementById('s_contact').value;
    var adhar = document.getElementById('adhar').value;
    var dob = document.getElementById('dob').value;
    var bed = document.getElementById('bed').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    $.ajax({
        type: 'POST',
        url: '/customer/add-temp-patient/',
        data: {
            'hospital': hospital,
            'name': name,
            'gender': gender,
            'p_mobile': p_mobile,
            's_mobile': s_mobile,
            'adhar': adhar,
            'dob': dob,
            'bed': bed,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            var added = res['added'];
            
            $('#exampleModal').modal('hide');
            get_bed_etails();   // get latest bed details

            if (added == true) {
                document.getElementById('alert').style.display = 'block';
                document.getElementById('alert').innerText = res['message'];
                setTimeout(function() {
                    document.getElementById('alert').style.display = "none";
                }, 3000);
            } else {
                document.getElementById('red-alert').style.display = 'block';
                document.getElementById('red-alert').innerHTML = res['message'] + "<button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Close\" id=\"custom-close-btn\" onclick=\"hide()\"></button>";
            }
            clear_form();
        }
    });
}

function clear_form() {
    document.getElementById('patient-name').value = "";
    document.getElementById('gender').value = "";
    document.getElementById('p_contact').value = "";
    document.getElementById('s_contact').value = "";
    document.getElementById('adhar').value = "";
    document.getElementById('dob').value = "";
    document.getElementById('bed').value = "";
}


function hide() {
    document.getElementById('red-alert').style.display = "none";
}


