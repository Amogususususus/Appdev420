from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from Medication_forms import CreateSyrupForm
import shelve, Customer
import Syrup
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from Forms import *


app = Flask(__name__)
app.secret_key = "123789123803ghj127891237831asd27891237892qwe3423423434234423234"

app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], message='File Not Allowed')])
    submit = SubmitField("Upload File")

@app.route('/')
def home():

    return render_template('homepage.html')



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
            print('Error')
        syrup = syrups_dict.get(id)
        file = form.file.data # First grab the file
        filename= secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        syrup.set_Picture(filename)
        db['Syrups'] = syrups_dict
        return redirect (url_for('retrieve_Syrup'))

    return render_template('Upload_Files.html', form=form)


@app.route('/Medication_Management', methods=['GET', 'POST'])
def create_Syrup():
    Create_Syrup_form = CreateSyrupForm(request.form)

    if request.method == 'POST' and Create_Syrup_form.validate():
        syrups_dict = {}
        db = shelve.open('syrup.db', 'c')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error')

        syrups_list = []
        for key in syrups_dict:
            syrup = syrups_dict.get(key)
            syrups_list.append(syrup)

        if len(syrups_dict) == 0:
            syrup = Syrup.Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                        Create_Syrup_form.Stock_Medication.data,
                        Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data,  len(syrups_dict))

        else:
            last_object = syrups_list[-1]
            syrup = Syrup.Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                        Create_Syrup_form.Stock_Medication.data,
                        Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data,  last_object.get_id())

        syrups_dict[syrup.get_id()] = syrup
        db['Syrups'] = syrups_dict

        return redirect (url_for('retrieve_Syrup'))

    return render_template('Medication_Management.html', form=Create_Syrup_form)

@app.route('/retrieveSyrup')
def retrieve_Syrup():
    syrups_dict = {}
    db = shelve.open('syrup.db', 'r')
    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error')


    syrups_list = []
    for key in syrups_dict:
        syrup = syrups_dict.get(key)
        syrups_list.append(syrup)

    Create_Syrup_form = CreateSyrupForm(request.form)
    if request.method == 'POST' and Create_Syrup_form.validate():
        return redirect (url_for('retrieve_Syrup'))
    return render_template('retrieveSyrup.html',count=len(syrups_list), syrups_list=syrups_list, form=Create_Syrup_form)

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
            print('Error')
        syrup = syrups_dict.get(id)
        syrup.set_name(Update_Syrup_form.Medication_name.data)
        syrup.set_price(Update_Syrup_form.Price_Medication.data)
        syrup.set_stock(Update_Syrup_form.Stock_Medication.data)
        syrup.set_Volume(Update_Syrup_form.Size.data)
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
        Update_Syrup_form.Description_Medication.data = syrup.get_Description()
        return render_template('UpdatingSyrups.html', form=Update_Syrup_form)

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
        print('Error')
    syrups_dict.pop(id)
    db['Syrups'] = syrups_dict

    return redirect(url_for('retrieve_Syrup'))

if __name__ == '__main__':
    app.run(debug=True)

#This is where Alan's code ends

#This is where Benson's code begins

@app.route('/findoutmore')
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
            return redirect(url_for('retrieve_customers'))
        else:
            for key in customers_dict:
                if login_form.email.data == customers_dict[key].get_email():
                    session['NRIC'] = customers_dict[key].get_nric()
                    session.pop('Admin',None)
                    return redirect(url_for('home')) #change home to booking form

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
    customers_dict = db['Customers']
    db.close()

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

if __name__ == '__main__':
    app.run(debug=True)
