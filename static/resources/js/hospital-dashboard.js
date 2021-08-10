window.onload = initAll();

function initAll() {
    build_web_socket();
    set_user_details();
    get_patients('Alive');
    get_bed_etails();
}


function set_user_details() {
    $.ajax({
        type: 'GET',
        url: '/userapp/get-user-details',
        dataType: 'json',
        
        success: function (res) {

            if (res['first_name'] == null) {
                document.getElementById('profile_name').innerText = res['username'];
                document.getElementById('page_title').innerText = res['username'] + ' - Dashboard';
                document.getElementById('profile_name_footer').innerHTML = "<div class=\"small\">Logged in as:</div>"+res['username']; 
            } else {
                document.getElementById('profile_name').innerText = res['first_name'] + ' ' + res['last_name'];
                document.getElementById('page_title').innerText = res['first_name'] + ' ' + res['last_name'] + '- Dashboard';
                document.getElementById('profile_name_footer').innerHTML = "<div class=\"small\">Logged in as:</div>" + res['first_name'] + " " + res['last_name'];
            }
            
            // if (res['profile_image_link'] == null) {
            //     document.getElementById('profile_image').src = 'https://i.postimg.cc/BbKp2Y9K/user.png';
            // } else {
            //     document.getElementById('profile_image').src = res['profile_image_link'];
            // }

        }
    });
}

function get_patients(slug) {
    $ ( document ).ready(function() {
        $.ajax({
            type: 'GET',
            url: '/hospital/get-patients/'+slug,
            dataType: 'json',
            
            success: function(res) {

                document.getElementById('databse_name').innerHTML = "<i class=\"fas fa-table mr-1\"></i>" + res['status'] + " Patients";      // change database table name

                var data = res['patients'];
                var table = $('#dataTable').DataTable();

                table.clear().draw();   // clear all rows

                for(i=0; i<data.length; i++) {
                    table.row.add( {
                        [0]:    "<a href=\"get-patient-info/" + data[i]['slug'] + "\">" + data[i]['name'] + "</a>",
                        [1]:    data[i]['adhar'],
                        [2]:    data[i]['status'],
                        [3]:    new Date(data[i]['created_at'])
                    } ).draw().node();
                }

                // set bed details
                document.getElementById('word-bed').innerText = 'Total beds: ' + res['word_bed'];
                document.getElementById('icu-bed').innerText = 'Total beds: ' + res['icu_bed'];
                document.getElementById('word_bed').value = res['word_bed'];
                document.getElementById('icu_bed').value = res['icu_bed'];
            }
        });
    });
}

function get_bed_etails() {

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
        document.getElementById('add-btn').disabled = true;
    } else {
        document.getElementById('add-btn').disabled = false;
    }
}


function add_patient() {
    var name = document.getElementById('patient_name').value;
    var gender = document.getElementById('gender').value;
    var p_mobile = document.getElementById('p_contact').value;
    var s_mobile = document.getElementById('s_contact').value;
    var adhar = document.getElementById('adhar').value;
    var dob = document.getElementById('dob').value;
    var bed = document.getElementById('bed').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    $.ajax({
        type: 'POST',
        url: '/hospital/add-patient/',
        data: {
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
            var data = res['added'];
            if (data == true) {
                get_patients('Alive');  // get updated patient list
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
                document.querySelector('.alert').style.display = 'block';
                document.querySelector('.alert').innerText = 'Patient added successfully.';
                clear_form();   // clear form
                setTimeout(function() {
                    document.querySelector('.alert').style.display = "none";
                }, 3000);
            } else {
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
                document.querySelector('.alert').style.display = 'block';
                document.querySelector('.alert').innerText = 'Can not add patient.';
                setTimeout(function() {
                    document.querySelector('.alert').style.display = "none";
                }, 3000);
            }
        }
    });
}

function clear_form() {
    document.getElementById('patient_name').value = "";
    document.getElementById('gender').value = "";
    document.getElementById('p_contact').value = "";
    document.getElementById('s_contact').value = "";
    document.getElementById('adhar').value = "";
    document.getElementById('dob').value = "";
}


function update_bed(bed_type) {
    var bed = document.getElementById(bed_type).value;
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    $.ajax({
        type: 'POST',
        url: '/hospital/update-bed/',
        data: {
            'bed': bed,
            'bed_type': bed_type,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            // set bed details
            document.getElementById('word-bed').innerText = 'Total beds: ' + res['word_bed'];
            document.getElementById('icu-bed').innerText = 'Total beds: ' + res['icu_bed'];
            document.getElementById('word_bed').value = res['word_bed'];
            document.getElementById('icu_bed').value = res['icu_bed'];  
            
            // update bed details
            get_bed_etails();
            
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
            document.querySelector('.alert').style.display = 'block';
            document.querySelector('.alert').innerText = 'Successfully update total number of bed.';
            setTimeout(function() {
                document.querySelector('.alert').style.display = "none";
            }, 3000);
        }
    });
}


function build_web_socket() {

    /* connection request */
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/bed-book/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        var notification = data['notification'];
        var id = data['id'];

        var container = document.getElementById('box');
        var content = "<div id=\"" + id + "\" class=\"notifications-item\"><div class=\"text\"><p>" + notification + "</p><button class=\"btn btn-primary my-btn\" onclick=\"patient_confirm_or_cancel('confirm', " + id + ")\">Confirm</button><button class=\"btn btn-danger my-btn\" onclick=\"patient_confirm_or_cancel('cancel', " + id + ")\">Cancel</button></div></div>";

        container.innerHTML += content;
    }
    
}

function patient_confirm_or_cancel(action, id) {
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    $.ajax({
        type: 'POST',
        url: '/bookpatient/add-new-bed/',
        data: {
            'action': action,
            'id': id,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            var status = res['status'];
            if (status == true) {
                document.getElementById(id).style.display = "none";     // hide clicked notification
                // get latest patients
                get_patients('Alive');
        
                document.querySelector('.alert').style.display = 'block';
                document.querySelector('.alert').innerText = res['message'];
                setTimeout(function() {
                    document.querySelector('.alert').style.display = "none";
                }, 3000);
            }
        }
    });
}


$(document).ready(function(){

    var down = false;
    
    $('#bell').click(function(e){
    
       var color = $(this).text();
        if(down){
    
            $('#box').css('height','0px');
            $('#box').css('opacity','0');
            down = false;
        }else{
    
            $('#box').css('height','auto');
            $('#box').css('opacity','1');
            down = true;
        }
    })
})


