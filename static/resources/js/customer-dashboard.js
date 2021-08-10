window.onload = initAll();

function initAll() {
    set_user_details();
    get_patients('Alive');
}


function set_user_details() {
    $.ajax({
        type: 'GET',
        url: '/userapp/get-user-details',
        dataType: 'json',
        
        success: function (res) {

            if (res['first_name'] == null) {
                document.getElementById('profile_name').innerText = res['username'];
                document.getElementById('page_title').innerText = res['username'] + '- Dashboard';
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
                        [0]:    "<a href=\"/hospital/get-patient-info/" + data[i]['slug'] + "\">" + data[i]['name'] + "</a>",
                        [1]:    data[i]['adhar'],
                        [2]:    data[i]['status'],
                        [3]:    new Date(data[i]['created_at'])
                    } ).draw().node();
                }
            }
        });
    });
}


function add_patient() {
    var hospital = document.getElementById('hospital_name').value;
    var name = document.getElementById('patient_name').value;
    var gender = document.getElementById('gender').value;
    var p_mobile = document.getElementById('p_contact').value;
    var s_mobile = document.getElementById('s_contact').value;
    var adhar = document.getElementById('adhar').value;
    var dob = document.getElementById('dob').value;

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
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            var added = res['added'];
            if (added == true) {
                console.log(res['hospital_id']);
            }

            console.log(res);


        }
    });
}


function search_hospitals() {
    var query_text = document.getElementById('search-field').value;
    var url = '/customer/search-hospitals?search=' + query_text;

    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        
        success: function (res) {
            var data = res;
            var body = document.getElementById('model-id');
            var content = data.map(item => 
                "<div class=\"content\"><p id=\"name-id\"><a href=\"/hospital/" + item.slug + "\">" + item.name + "</a></p><p id=\"address-id\">" + item.address + "</p></div>"
                );
            
            body.innerHTML = content;
        }
    });
}
