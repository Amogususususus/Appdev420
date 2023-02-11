from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from Medication_forms import CreateSyrupForm, SearchForm, UploadFileForm, Adding_Stock_Form, FilterForm, itemform, orderform
import Customer
import Syrup
from Account_Form import *
from Meeting_Form import AppointmentForm, updateAppointmentForm
import Appointment
from Forms2 import CreateFeedbackForm
import shelve, Feedback
from Syrup import *
from datetime import date

app = Flask(__name__)
app.secret_key = "123789123803ghj127891237831asd27891237892qwe3423423434234423234"

app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
################################here begins Helun's code#################################

NameSearchList = []
List_Sorting = []
List_Sorting_Final = []
current_cart=[]

def SortStock():
    List_Sorting.clear()
    List_Sorting_Final.clear()

    syrups_dict = {}
    db = shelve.open('syrup.db')

    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error in handling database!')

    for i in syrups_dict:
        syrup = syrups_dict.get(i)
        stock = syrup.get_stock()

        if stock not in List_Sorting:
            List_Sorting.append(stock)
            List_Sorting.sort()



    for i in List_Sorting:
        for key in syrups_dict:
            syrups = syrups_dict.get(key)
            if syrups.get_stock() == int(i):
                if syrups not in List_Sorting_Final:
                    List_Sorting_Final.append((syrups))





def SearchFunction(searchItem):

    NameSearchList.clear()

    syrups_dict = {}
    db = shelve.open('syrup.db')

    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error in handling database!')

    try:
        searchData = str(searchItem).lower()

    except:
        searchData = str(searchItem).lower()


    for key in syrups_dict:
        syrup = syrups_dict.get(key)

        if isinstance(searchData, str):
            if searchData == syrup.get_name() or searchData in str(syrup.get_name()).lower():
                NameSearchList.append(syrup)




@app.route('/')
def home():

    return render_template('home.html')
@app.route('/User_Homepage')
def User_Homepage():

    return render_template('User_Homepage.html')
@app.route('/findoutmore')
def findoutmore():

    return render_template('findoutmore.html')

@app.route('/Upload_Files/<int:id>/' ,methods=['GET','POST'])
def Upload_Files(id):
    form = UploadFileForm()
    if request.method == 'POST' and form.validate_on_submit():
        syrups_dict = {}
        db = shelve.open('syrup.db', 'w')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')
        syrup = syrups_dict.get(id)
        file = form.file.data # First grab the file
        filename= secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        syrup.set_Picture(filename)
        db['Syrups'] = syrups_dict
        flash('Medication Already Exists, use a different name!', 'NameAlreadyExistError')
        return redirect (url_for('retrieve_Syrup'))

    return render_template('Upload_Files.html', form=form)


@app.route('/Medication_Management', methods=['GET', 'POST'])
def create_Syrup():
    Create_Syrup_form = CreateSyrupForm(request.form)
    if request.method == 'POST' and Create_Syrup_form.validate_on_submit():
        syrups_dict = {}
        db = shelve.open('syrup.db', 'c')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')

        syrups_list_names = []
        for key in syrups_dict:
            syrupname = syrups_dict.get(key)
            Medic_Name = syrupname.get_name()
            syrups_list_names.append(Medic_Name)

        syrups_list = []
        for key in syrups_dict:
            syrup = syrups_dict.get(key)
            syrups_list.append(syrup)

        if Create_Syrup_form.Medication_name.data not in syrups_list_names:

            if len(syrups_dict) == 0:
                syrup = Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                            Create_Syrup_form.Stock_Medication.data,
                            Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data, Create_Syrup_form.Expiration.data, len(syrups_dict))

            else:
                last_object = syrups_list[-1]
                syrup = Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                            Create_Syrup_form.Stock_Medication.data,
                            Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data, Create_Syrup_form.Expiration.data, last_object.get_id())

            syrups_dict[syrup.get_id()] = syrup
            db['Syrups'] = syrups_dict
            return redirect (url_for('retrieve_Syrup'))
        else:
            flash('Medication Already Exists, use a different name!', 'NameAlreadyExistError')

    return render_template('Medication_Management.html', form=Create_Syrup_form)

@app.route('/retrieveSyrup', methods=['GET', 'POST'])
def retrieve_Syrup():

    Searchingform = SearchForm()
    form = FilterForm()

    if Searchingform.validate_on_submit() and request.method == 'POST':

        syrups_dict = {}
        db = shelve.open('syrup.db', 'r')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')

        SearchData = Searchingform.searched.data

        SearchFunction(SearchData)

        NameList_searchPage = NameSearchList


        return render_template('retrieveSyrup.html', Searchingform=Searchingform, ListofNames=NameList_searchPage, count=len(NameSearchList), form=form)

    if form.validate_on_submit() and request.method == 'POST':
        if form.Filter.data == 'filtered':
            SortStock()

            sortedList=List_Sorting_Final

            return render_template('retrieveSyrup.html', form=form, countforsortList=len(List_Sorting_Final), SortedFinalList=sortedList, Searchingform=Searchingform)


    syrups_dict = {}
    db = shelve.open('syrup.db', 'r')
    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error, database for medication cannot be retrieved')

    syrups_list = []
    for key in syrups_dict:
        syrup = syrups_dict.get(key)
        syrups_list.append(syrup)



    return render_template('retrieveSyrup.html',count=len(syrups_list), syrups_list=syrups_list, Searchingform=Searchingform, form=form)

@app.route('/Order_Medication', methods=['GET', 'POST'])
def Order_Medication():

    Searchingform = SearchForm()
    form = FilterForm()

    if Searchingform.validate_on_submit() and request.method == 'POST':

        syrups_dict = {}
        db = shelve.open('syrup.db', 'r')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')

        SearchData = Searchingform.searched.data

        SearchFunction(SearchData)

        NameList_searchPage = NameSearchList


        return render_template('Order_Medication.html', Searchingform=Searchingform, ListofNames=NameList_searchPage, count=len(NameSearchList), form=form)


    syrups_dict = {}
    db = shelve.open('syrup.db', 'r')
    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error, database for medication cannot be retrieved')

    syrups_list = []
    for key in syrups_dict:
        syrup = syrups_dict.get(key)
        syrups_list.append(syrup)

    return render_template('Order_Medication.html',count=len(syrups_list), syrups_list=syrups_list, Searchingform=Searchingform, form=form)

@app.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):

    form=itemform()

    if request.method == 'POST' and form.validate_on_submit():
        syrups_dict = {}
        productdict={}
        syrupdict={}
        db = shelve.open('syrup.db', 'r')
        syrups_dict = db['Syrups']

        syrup=syrups_dict.get(id)
        theid=syrup.get_id()
        count=-1
        if current_cart == []:
            name=syrup.get_name()
            price=syrup.get_price()
            Quantity=form.quantity.data
            syrupdict["Name"]=name
            syrupdict["Price"]=price
            syrupdict["Quantity"]=Quantity
            productdict[syrup.get_id()] = syrupdict
            current_cart.append(productdict)

        else:
            for i in current_cart:
                count+=1

                keys = i.keys()

                for key in keys:
                    key=key

                if theid == key:

                    existing=current_cart[count][key]['Quantity']
                    new=int(form.quantity.data)
                    final=int(existing)+int(new)
                    current_cart[count][key]['Quantity']=final
                    productdict={}
                    break

                elif theid != key:

                    name=syrup.get_name()
                    price=syrup.get_price()
                    Quantity=form.quantity.data
                    syrupdict["Name"]=name
                    syrupdict["Price"]=price
                    syrupdict["Quantity"]=Quantity
                    productdict[syrup.get_id()] = syrupdict


            if productdict != {}:
                current_cart.append(productdict)


        return redirect (url_for('Order_Medication'))

    return render_template('Product_Medication.html', form=form)

@app.route('/Cart')
def retrieve_cart():
    form=orderform()
    cart=[]
    if  request.method == 'POST' and form.validate_on_submit():
        recname=form.name.data
        address=form.address.data
        current_cart.append(recname)
        current_cart.append(address)
        Order_dict = {}
        db = shelve.open('Order', 'c')
        try:
            if 'Orders' in db:
                Order_dict = db['Orders']
            else:
                db['Orders'] = Order_dict
        except:
            print('Error, database for medication cannot be retrieved')

        db['receiptid']=current_cart



        return render_template('Cart.html', cart=cart, form=form)

    items=current_cart
    for i in items:

        keys = i.keys()
        for key in keys:

            i[key]['id']=key

            cart.append(i[key])

    countoflist=len(cart)
    print(current_cart)
    return render_template('Cart.html', cart=cart, count=countoflist, form=form)

@app.route('/Update_Quantity/<int:id>/', methods=['GET', 'POST'])
def Update_Quantity(id):
    Update_form = itemform()
    if request.method == 'POST' and Update_form.validate_on_submit():
        items=current_cart
        count=-1
        for i in items:
            count+=1
            if id in i:
                break
        new=Update_form.quantity.data

        items[count][id]['Quantity']=new

        return redirect (url_for('retrieve_cart'))
    return render_template('Update_Quantity.html', form=Update_form)

@app.route('/delete_items/<int:id>', methods=['POST'])
def delete_items(id):
    count = 0
    for item in current_cart:
        for key in item:
            if key == id:
                del current_cart[count]
                count += 1
                break
            else:
                count += 1

    return redirect(url_for('retrieve_cart'))

@app.route('/UpdatingSyrups/<int:id>/', methods=['GET', 'POST'])
def update_Syrup(id):
    Update_Syrup_form = CreateSyrupForm(request.form)
    if request.method == 'POST' and Update_Syrup_form.validate():
        syrups_dict = {}
        db = shelve.open('syrup.db', 'w')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')
        syrup = syrups_dict.get(id)
        syrup.set_name(Update_Syrup_form.Medication_name.data)
        syrup.set_price(Update_Syrup_form.Price_Medication.data)
        syrup.set_stock(Update_Syrup_form.Stock_Medication.data)
        syrup.set_Volume(Update_Syrup_form.Size.data)
        syrup.Set_Expiry(Update_Syrup_form.Expiration.data)
        syrup.set_Description(Update_Syrup_form.Description_Medication.data)
        db['Syrups'] = syrups_dict

        return redirect (url_for('retrieve_Syrup'))
    else:
        syrups_dict = {}
        db = shelve.open('syrup.db', 'r')
        syrups_dict = db['Syrups']

        syrup = syrups_dict.get(id)
        Update_Syrup_form.Medication_name.data = syrup.get_name()
        Update_Syrup_form.Price_Medication.data = syrup.get_price()
        Update_Syrup_form.Stock_Medication.data = syrup.get_stock()
        Update_Syrup_form.Size.data = syrup.get_Volume()
        Update_Syrup_form.Expiration.data = syrup.get_Expiry()
        Update_Syrup_form.Description_Medication.data = syrup.get_Description()
        return render_template('UpdatingSyrups.html', form=Update_Syrup_form)

@app.route('/Add_Stock/<int:id>/' ,methods=['GET','POST'])
def Add_Stock(id):
    form = Adding_Stock_Form()
    if request.method == 'POST' and form.validate_on_submit():
        syrups_dict = {}
        db = shelve.open('syrup.db', 'w')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')

        syrup = syrups_dict.get(id)
        Current_Stock_Value=syrup.get_stock()
        Addition_Value=form.Addition_Value.data
        New_Stock=Addition_Value+Current_Stock_Value
        syrup.set_stock(New_Stock)
        db['Syrups'] = syrups_dict

        return redirect (url_for('retrieve_Syrup'))
    return render_template('Add_Stock.html', form=form)


@app.route('/delete_syrups/<int:id>', methods=['POST'])
def delete_syrup(id):
    syrups_dict = {}
    db = shelve.open('syrup.db', 'w')
    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error, database for medication cannot be retrieved')
    syrups_dict.pop(id)
    db['Syrups'] = syrups_dict

    return redirect(url_for('retrieve_Syrup'))

###########################This is where Helun's code ends###########################

##########################This is where Benson's code begins########################

@app.route('/findoutmore.html')
def aboutus():
    return render_template('findoutmore.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():

        customers_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")



        if login_form.email.data == "admin@mail.com" and login_form.password.data == "Iloveappdev":
            session["Admin"] = login_form.email.data
            return redirect(url_for('retrieve_appointments_admin'))
        else:
            for key in customers_dict:
                if login_form.email.data == customers_dict[key].get_email():
                    session['NRIC'] = customers_dict[key].get_nric()
                    session.pop('Admin',None)
                    return redirect(url_for('User_Homepage')) #change home to booking form

    return render_template('login.html', form=login_form)

@app.route('/register', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.name.data,
                                     create_customer_form.gender.data,
                                     create_customer_form.membership.data,
                                     create_customer_form.condition.data,
                                     create_customer_form.email.data,
                                     create_customer_form.age.data,
                                     create_customer_form.address.data,
                                     create_customer_form.password.data,
                                     create_customer_form.nric.data)
##        customers_dict[customer.get_customer_id()] = customer
        customers_dict[customer.get_user_id()] = customer
        db['Customers'] = customers_dict




        db.close()

        return redirect(url_for('login'))
    return render_template('register.html', form=create_customer_form)



@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    try:
        if 'Customers' in db:
            customers_dict = db['Customers']
        else:
            db['Customers'] = customers_dict
    except:
        print('Error')

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)

@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_condition(update_customer_form.condition.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_age(update_customer_form.age.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_password(update_customer_form.password.data)
        customer.set_nric(update_customer_form.nric.data)


        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.membership.data = customer.get_membership()
        update_customer_form.condition.data = customer.get_condition()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.age.data = customer.get_age()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.password.data = customer.get_password()
        update_customer_form.nric.data = customer.get_nric()



        return render_template('updateCustomer.html', form=update_customer_form)

@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

###############This is where Benson's code ends###################################

####################This is where Isaac's code begins#######################################

# CUSTOMER SIDE
today = date.today()
@app.route('/createAppointment', methods=['GET', 'POST'])
def create_appointment():
    create_appointment_form = AppointmentForm(request.form)
    if request.method == 'POST' and create_appointment_form.validate():
        appointments_dict = {}
        db = shelve.open('appointment.db', 'c')

        try:
            if 'Appointments' in db:
                appointments_dict = db['Appointments']
            else:
                db['Appointments'] = appointments_dict

        except:
            print("Error in retrieving Appointments from appointment.db.")

        appointments_list = []
        for key in appointments_dict:
            appointment = appointments_dict.get(key)
            appointments_list.append(appointment)

        if len(appointments_dict) == 0:
            appointment = Appointment.Appointment(create_appointment_form.name_ment.data,
                                                  create_appointment_form.age_ment.data,
                                                  create_appointment_form.gender_ment.data,
                                                  create_appointment_form.nric_ment.data,
                                                  create_appointment_form.email_ment.data,
                                                  create_appointment_form.address_ment.data,
                                                  create_appointment_form.remarks_ment.data,
                                                  create_appointment_form.past_condition_ment.data,
                                                  create_appointment_form.doctor_ment.data,
                                                  create_appointment_form.date_ment.data,
                                                  create_appointment_form.time_ment.data,
                                                  create_appointment_form.attendance_ment.data,
                                                  create_appointment_form.meeting_status_ment.data,
                                                  len(appointments_dict))

        else:
            last_object = appointments_list[-1]
            appointment = Appointment.Appointment(create_appointment_form.name_ment.data,
                                                  create_appointment_form.age_ment.data,
                                                  create_appointment_form.gender_ment.data,
                                                  create_appointment_form.nric_ment.data,
                                                  create_appointment_form.email_ment.data,
                                                  create_appointment_form.address_ment.data,
                                                  create_appointment_form.remarks_ment.data,
                                                  create_appointment_form.past_condition_ment.data,
                                                  create_appointment_form.doctor_ment.data,
                                                  create_appointment_form.date_ment.data,
                                                  create_appointment_form.time_ment.data,
                                                  create_appointment_form.attendance_ment.data,
                                                  create_appointment_form.meeting_status_ment.data,
                                                  last_object.get_id())

        appointments_dict[appointment.get_id()] = appointment
        db['Appointments'] = appointments_dict

        db.close()

        return redirect(url_for('retrieve_appointments'))
    return render_template('createAppointment.html', form=create_appointment_form)

@app.route('/retrieveAppointments')
def retrieve_appointments():
    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)
        if appointment.get_meeting_status_ment() != 'Over':
            if appointment.get_date_ment().strftime("%Y-%m-%d") > today.strftime("%Y-%m-%d") or appointment.get_date_ment().strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
                appointments_list.append(appointment)

    return render_template('retrieveAppointments.html', count=len(appointments_list), appointments_list=appointments_list)

@app.route('/updateAppointment/<int:id>/', methods=['GET', 'POST'])
def update_appointment(id):
    update_appointment_form = updateAppointmentForm(request.form)
    if request.method == 'POST' and update_appointment_form.validate():
        appointments_dict = {}
        db = shelve.open('appointment.db', 'w')
        appointments_dict = db['Appointments']

        appointment = appointments_dict.get(id)
        appointment.set_name_ment(update_appointment_form.name_ment.data)
        appointment.set_age_ment(update_appointment_form.age_ment.data)
        appointment.set_gender_ment(update_appointment_form.gender_ment.data)
        appointment.set_nric_ment(update_appointment_form.nric_ment.data)
        appointment.set_email_ment(update_appointment_form.email_ment.data)
        appointment.set_address_ment(update_appointment_form.address_ment.data)
        appointment.set_remarks_ment(update_appointment_form.remarks_ment.data)
        appointment.set_past_condition_ment(update_appointment_form.past_condition_ment.data)
        appointment.set_doctor_ment(update_appointment_form.doctor_ment.data)
        appointment.set_date_ment(update_appointment_form.date_ment.data)
        appointment.set_time_ment(update_appointment_form.time_ment.data)
        appointment.set_attendance_ment(update_appointment_form.attendance_ment.data)
        appointment.set_meeting_status_ment(update_appointment_form.meeting_status_ment.data)

        db['Appointments'] = appointments_dict

        db.close()

        return redirect(url_for('retrieve_appointments'))
    else:
        appointments_dict = {}
        db = shelve.open('appointment.db', 'r')
        appointments_dict = db['Appointments']

        db.close()

        appointment = appointments_dict.get(id)
        update_appointment_form.name_ment.data = appointment.get_name_ment()
        update_appointment_form.age_ment.data = appointment.get_age_ment()
        update_appointment_form.gender_ment.data = appointment.get_gender_ment()
        update_appointment_form.nric_ment.data = appointment.get_nric_ment()
        update_appointment_form.email_ment.data = appointment.get_email_ment()
        update_appointment_form.address_ment.data = appointment.get_address_ment()
        update_appointment_form.remarks_ment.data = appointment.get_remarks_ment()
        update_appointment_form.past_condition_ment.data = appointment.get_past_condition_ment()
        update_appointment_form.doctor_ment.data = appointment.get_doctor_ment()
        update_appointment_form.date_ment.data = appointment.get_date_ment()
        update_appointment_form.time_ment.data = appointment.get_time_ment()
        update_appointment_form.attendance_ment.data = appointment.get_attendance_ment()
        update_appointment_form.meeting_status_ment.data = appointment.get_meeting_status_ment()

        return render_template('updateAppointment.html', form=update_appointment_form)

@app.route('/deleteAppointment/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    appointments_dict.pop(id)

    db['Appointments'] = appointments_dict
    db.close()

    return redirect(url_for('retrieve_appointments'))

# ADMIN SIDE
@app.route('/Admin_Homepage')
def retrieve_appointments_admin():
    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)
        if appointment.get_meeting_status_ment() != 'Over':
            if appointment.get_date_ment().strftime("%Y-%m-%d") > today.strftime("%Y-%m-%d") or appointment.get_date_ment().strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
                appointments_list.append(appointment)

    return render_template('Admin_Homepage.html', count=len(appointments_list), appointments_list=appointments_list)

@app.route('/updateAppointmentAdmin/<int:id>/', methods=['GET', 'POST'])
def update_appointment_admin(id):
    update_appointment_admin_form = updateAppointmentForm(request.form)
    if request.method == 'POST' and update_appointment_admin_form.validate():
        appointments_dict = {}
        db = shelve.open('appointment.db', 'w')
        appointments_dict = db['Appointments']

        appointment = appointments_dict.get(id)
        appointment.set_name_ment(update_appointment_admin_form.name_ment.data)
        appointment.set_age_ment(update_appointment_admin_form.age_ment.data)
        appointment.set_gender_ment(update_appointment_admin_form.gender_ment.data)
        appointment.set_nric_ment(update_appointment_admin_form.nric_ment.data)
        appointment.set_email_ment(update_appointment_admin_form.email_ment.data)
        appointment.set_address_ment(update_appointment_admin_form.address_ment.data)
        appointment.set_remarks_ment(update_appointment_admin_form.remarks_ment.data)
        appointment.set_past_condition_ment(update_appointment_admin_form.past_condition_ment.data)
        appointment.set_doctor_ment(update_appointment_admin_form.doctor_ment.data)
        appointment.set_date_ment(update_appointment_admin_form.date_ment.data)
        appointment.set_time_ment(update_appointment_admin_form.time_ment.data)
        appointment.set_attendance_ment(update_appointment_admin_form.attendance_ment.data)
        appointment.set_meeting_status_ment(update_appointment_admin_form.meeting_status_ment.data)

        db['Appointments'] = appointments_dict

        db.close()

        return redirect(url_for('retrieve_appointments_admin'))
    else:
        appointments_dict = {}
        db = shelve.open('appointment.db', 'r')
        appointments_dict = db['Appointments']

        db.close()

        appointment = appointments_dict.get(id)
        update_appointment_admin_form.name_ment.data = appointment.get_name_ment()
        update_appointment_admin_form.age_ment.data = appointment.get_age_ment()
        update_appointment_admin_form.gender_ment.data = appointment.get_gender_ment()
        update_appointment_admin_form.nric_ment.data = appointment.get_nric_ment()
        update_appointment_admin_form.email_ment.data = appointment.get_email_ment()
        update_appointment_admin_form.address_ment.data = appointment.get_address_ment()
        update_appointment_admin_form.remarks_ment.data = appointment.get_remarks_ment()
        update_appointment_admin_form.past_condition_ment.data = appointment.get_past_condition_ment()
        update_appointment_admin_form.doctor_ment.data = appointment.get_doctor_ment()
        update_appointment_admin_form.date_ment.data = appointment.get_date_ment()
        update_appointment_admin_form.time_ment.data = appointment.get_time_ment()
        update_appointment_admin_form.attendance_ment.data = appointment.get_attendance_ment()
        update_appointment_admin_form.meeting_status_ment.data = appointment.get_meeting_status_ment()

        return render_template('updateAppointmentAdmin.html', form=update_appointment_admin_form)

@app.route('/openRoomAdmin/<int:id>', methods=['POST'])
def open_room_admin(id):
    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    appointment = appointments_dict.get(id)
    appointment.set_meeting_status_ment('Open')

    db['Appointments'] = appointments_dict
    db.close()

    return redirect(url_for('retrieve_appointments_admin'))

@app.route('/deleteAppointmentAdmin/<int:id>', methods=['POST'])
def delete_appointment_admin(id):
    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

#   appointments_dict.pop(id)
    appointment = appointments_dict.get(id)
    appointment.set_meeting_status_ment('Over')

    db['Appointments'] = appointments_dict
    db.close()

    return redirect(url_for('retrieve_appointments_admin'))

@app.route('/retrievePastAppointmentsAdmin')
def retrieve_past_appointments_admin():
    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)

        if appointment.get_date_ment().strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d") or appointment.get_meeting_status_ment() == 'Over':
            appointments_list.append(appointment)

    return render_template('retrievePastAppointmentsAdmin.html', count=len(appointments_list), appointments_list=appointments_list)

@app.route('/changeAttendanceToUnattended/<int:id>', methods=['POST'])
def change_to_unattended(id):
    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    appointment = appointments_dict.get(id)
    appointment.set_attendance_ment('Unattended')

    db['Appointments'] = appointments_dict
    db.close()

    return redirect(url_for('retrieve_past_appointments_admin'))

@app.route('/changeAttendanceToAttended/<int:id>', methods=['POST'])
def change_to_attended(id):
    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    appointment = appointments_dict.get(id)
    appointment.set_attendance_ment('Attended')

    db['Appointments'] = appointments_dict
    db.close()

    return redirect(url_for('retrieve_past_appointments_admin'))

@app.route('/retrieveUnattendedAppointmentsAdmin')
def retrieve_unattended_appointments_admin():
    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)

        if appointment.get_attendance_ment() == 'Unattended':
            appointments_list.append(appointment)

    return render_template('retrieveUnattendedAppointmentsAdmin.html', count=len(appointments_list), appointments_list=appointments_list)

###############This is where Isaac's code ends###################################

####################This is where Jai's code begins#######################################

@app.route('/createFeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedbacks']
        except:
            print("Error in retrieving Feedback from feedback.db.")

        feedback = Feedback.Feedback(create_feedback_form.date.data, create_feedback_form.name.data, create_feedback_form.email.data, create_feedback_form.typeqn.data, create_feedback_form.qn1.data, create_feedback_form.qn2.data)
        feedback_dict[feedback.get_feedback_id()] = feedback
        db['Feedbacks'] = feedback_dict

        db.close()

        return redirect(url_for('User_Homepage'))
    return render_template('createFeedback.html', form=create_feedback_form)


@app.route('/retrieveFeedback')
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedbacks']
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)

    return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list)



@app.route('/updateFeedback/<int:id>/', methods=['GET', 'POST'])
def update_feedback(id):
    update_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and update_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'w')
        feedback_dict = db['Feedbacks']

        feedback = feedback_dict.get(id)
        feedback.set_date(update_feedback_form.date.data)
        feedback.set_name(update_feedback_form.name.data)
        feedback.set_email(update_feedback_form.email.data)
        feedback.set_typeqn(update_feedback_form.typeqn.data)
        feedback.set_qn1(update_feedback_form.qn1.data)
        feedback.set_qn2(update_feedback_form.qn2.data)

        db['Feedbacks'] = feedback_dict
        db.close()

        return redirect(url_for('User_Homepage'))
    else:
        feedback_dict = {}
        db = shelve.open('feedback.db', 'r')
        feedback_dict = db['Feedbacks']
        db.close()

        feedback = feedback_dict.get(id)
        update_feedback_form.date.data = feedback.get_date()
        update_feedback_form.name.data = feedback.get_name()
        update_feedback_form.email.data = feedback.get_email()
        update_feedback_form.typeqn.data = feedback.get_typeqn()
        update_feedback_form.qn1.data = feedback.get_qn1()
        update_feedback_form.qn2.data = feedback.get_qn2()

        return render_template('updateFeedback.html', form=update_feedback_form)



@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedback_dict = db['Feedbacks']

    feedback_dict.pop(id)

    db['Feedbacks'] = feedback_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
###############This is where Jai's code ends###################################
