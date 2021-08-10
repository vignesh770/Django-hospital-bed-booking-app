# Proect Title:   BookYourBed

# Project Description:  
    This is a very helpful project in this pandemic where users can apply for word and icu type bed for covid affected patients to any hospital online. Any user after creating their account can apply for bed for covid affected patients. After applying, the hospital authority will get a notification, if they confirm this request then one bed will be booked for this patient and the user will get a confirmation mail. This mail information will be used to admit the patient in the hospital. If the hospital authority cancels this request then the user will get a cancellation mail and the user can apply again for bed.
    Here we provide a new feature that any user can apply maximum two beds for each covid patient in two different hospitals but the bed type must be the same, then notification will be sent to both the hospitals selected by the user. If one hospital authority confirms the bed request then another request will automatically be deleted.

# Software Requirements:
    1. Code editor(VS code)
    2. Browser(Chrome)
    3. git(version control)

# Process Flow:
    In this project, there have two sides. These are,

    1. Hospital authority side
        First of all we have to register Hospital with the following credentials:
            1. Hospital name
            2. Hospital Id
            3. Email
            4. help line no
            5. Address
            6. State
            7. City
            8. Username
            9. Password
        after successfull registration we will rediret to the hospital dashboard page. In this dashboard page at first we have to update the numbers of total ICU and Word bed(default is 0). If we do not update the bed numbers then this hospital will not be show in the user search list. So, we have to update the total number of bed. Hospital authority can add any patient from this dashboard. After adding a patient this patient details will directly save in the patient table and authority will get a success screen message(patien added successfully). Authority can edit the patient details and can update patient status(Alive, Success, Dead).

    2. User side
        In the user side, we have to register a user account(guest account or sign-up with google account). After registration user will redirect to the user dashboard page. In this dashboard page user can search hospital with their name, address, city, state. User can click on any hospital name and redirect to the hospital inner page. In this page user can make a bed request for any patient. User can apply maximum two beds for each patient in two different hospital but the bed type must be same. After applying for bed request user will see a success screen(Request has been send for bed) and one notification will popup in the hospital dashboard page. In this section we store the request and the patient details to a temp database. If the authority confirm the bed request then we create a confirm request foreignkey with this request and also we store the patient into the patient table and a confirmation mail will be send to the user's email id and user can see the patient details in the patient table in the dashboard. If authority cancel the bad request then we create a cancel request foreignkey with this request and also we delete the temp patient details from the temp database and one cancellation mail will be send to the user's email.

