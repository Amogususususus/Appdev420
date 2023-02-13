from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename
import os
from Medication_forms import CreateSyrupForm, SearchForm, UploadFileForm, Adding_Stock_Form, FilterForm, itemform, orderform
import Customer
import Syrup
from Account_Form import *
from Meeting_Form import AppointmentForm, updateAppointmentForm, DoctorFilterForm
import Appointment
from Forms2 import CreateFeedbackForm
import shelve, Feedback
from Syrup import *
from datetime import date

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    return render_template('User_Homepage.html')
@app.route('/findoutmore')
def findoutmore():

    return render_template('findoutmore.html')

@app.route('/Upload_Files/<int:id>/' ,methods=['GET','POST'])
def Upload_Files(id):
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

    form=itemform()

    if request.method == 'POST' and form.validate_on_submit():
        syrups_dict = {}
        productdict={}
        syrupdict={}
        db = shelve.open('syrup.db')
        syrups_dict = db['Syrups']
        syrup=syrups_dict.get(id)
        Subtract=syrup.get_stock()
        Quantity=form.quantity.data
        theid=syrup.get_id()
        count=-1
        if Quantity > Subtract:
            return redirect(url_for('sorry_validate'))
        else:
            if current_cart == []:
                name=syrup.get_name()
                price=syrup.get_price()
                Quantity=form.quantity.data
                Total=price*Quantity
                syrupdict["Name"]=name
                syrupdict["Price"]=price
                syrupdict["Quantity"]=Quantity
                syrupdict["Total"]=Total
                productdict[syrup.get_id()] = syrupdict
                current_cart.append(productdict)
                Subtract=syrup.get_stock()
                New_Value=Subtract-Quantity
                syrup.set_stock(New_Value)

                db['Syrups']=syrups_dict
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

                        Subtract=syrup.get_stock()

                        New_Value=Subtract-new
                        syrup.set_stock(New_Value)

                        print(syrup.get_stock())
                        db['Syrups']=syrups_dict
                        break

                    elif theid != key:

                        name=syrup.get_name()
                        price=syrup.get_price()
                        Quantity=form.quantity.data
                        Total=price*Quantity
                        syrupdict["Name"]=name
                        syrupdict["Price"]=price
                        syrupdict["Quantity"]=Quantity
                        syrupdict["Total"]=Total
                        productdict[syrup.get_id()] = syrupdict
                        Subtract=syrup.get_stock()
                        New_Value=Subtract-Quantity
                        syrup.set_stock(New_Value)

                        db['Syrups']=syrups_dict
                if productdict != {}:
                    current_cart.append(productdict)


            return redirect (url_for('Order_Medication'))

    return render_template('Product_Medication.html', form=form)

@app.route('/Cart', methods=['GET', 'POST'])
def retrieve_cart():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

    form=orderform()
    cart=[]
    summary=0
    if  request.method == 'POST':
        recname=form.name.data
        address=form.address.data
        current_cart.append(recname)
        current_cart.append(address)
        Order_dict = {}

        dbOrder = shelve.open('Order', 'c')
        try:
            if 'Orders' in dbOrder:
                Order_dict = dbOrder['Orders']
            else:
                dbOrder['Orders'] = Order_dict
        except:
            print('Error, database for medication cannot be retrieved')


        Order_list = []
        for key in Order_dict:
            Order = Order_dict.get(key)
            Order_list.append(Order)

        if len(Order_dict) == 0:
            id=len(Order_dict)

        else:
            last_object = len(Order_list)
            id=last_object
        Order_dict[id] = current_cart
        dbOrder['Orders'] = Order_dict

        current_cart.clear()


        return redirect (url_for('Order_Requests'))

    else:
        items=current_cart
        for i in items:
            keys = i.keys()
            for key in keys:
                i[key]['id']=key
                cart.append(i[key])
                summary+=i[key]['Total']


        countoflist=len(cart)
        return render_template('Cart.html', cart=cart, count=countoflist, form=form, sum=summary)

@app.route('/Update_Quantity/<int:id>/', methods=['GET', 'POST'])
def Update_Quantity(id):
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

    Update_form = itemform()
    if request.method == 'POST' and Update_form.validate_on_submit():
        syrups_dict = {}
        db = shelve.open('syrup.db', 'w')
        try:
            if 'Syrups' in db:
                syrups_dict = db['Syrups']
            else:
                db['Syrups'] = syrups_dict
        except:
            print('Error, database for medication cannot be retrieved')

        items=current_cart
        count=-1
        for i in items:
            count+=1
            if id in i:
                break
        new=Update_form.quantity.data



        syrup=syrups_dict.get(id)
        old=current_cart[0][id]['Quantity']
        stock=syrup.get_stock()
        x = new - old
        final=stock - x
        syrup.set_stock(final)
        db['Syrups'] = syrups_dict
        items[count][id]['Quantity']=new
        return redirect (url_for('retrieve_cart'))
    return render_template('Update_Quantity.html', form=Update_form)

@app.route('/delete_items/<int:id>', methods=['POST'])
def delete_items(id):
    syrups_dict = {}
    db = shelve.open('syrup.db', 'w')
    try:
        if 'Syrups' in db:
            syrups_dict = db['Syrups']
        else:
            db['Syrups'] = syrups_dict
    except:
        print('Error, database for medication cannot be retrieved')

    syrup=syrups_dict.get(id)

    Add=current_cart[0][id]['Quantity']
    current=syrup.get_stock()
    Final=current+Add
    syrup.set_stock(Final)
    db['Syrups'] = syrups_dict
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

@app.route('/Order_Requests')
def Order_Requests():
    count=0
    Order_dict={}
    items_list=[]
    Final_items_list=[]
    db = shelve.open('Order')
    try:
        if 'Orders' in db:
            Order_dict = db['Orders']
        else:
            db['Orders'] = Order_dict
    except:
        print('Error, database for medication cannot be retrieved')
    for k in range(0, len(Order_dict)):
        items=Order_dict
        c=items[k]
        for i in range(0, len(c)-2):
            item=c[i]
            keys = item.keys()
            for key in keys:
                a=item[key]
                a['id']=count
                a['name']=c[len(c)-2]
                a['address']=c[len(c)-1]

                items_list.append(a)

        count+=1
        Final_items_list.append(items_list)

        items_list=[]
    return render_template('Order_Requests.html', items_list=Final_items_list)


@app.route('/Delete_Order/<int:id>/', methods=['POST'])
def Delete_Order(id):

    Order_dict={}

    db = shelve.open('Order')
    try:
        if 'Orders' in db:
            Order_dict = db['Orders']
        else:
            db['Orders'] = Order_dict
    except:
        print('Error, database for medication cannot be retrieved')

    Order_dict.pop(id)
    db['Orders'] = Order_dict

    return redirect (url_for('Order_Requests'))

@app.route('/Overflow_Validate')
def sorry_validate():

    return render_template('sorry.html')

@app.route('/UpdatingSyrups/<int:id>/', methods=['GET', 'POST'])
def update_Syrup(id):
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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

        if login_form.nric.data == "ADMIN" and login_form.password.data == "Iloveappdev":
            session["NRIC"] = 'ADMIN'
            return redirect(url_for('retrieve_appointments_admin'))
        else:
            for key in customers_dict:
                if login_form.nric.data == customers_dict[key].get_nric():
                    session["NRIC"] = customers_dict[key].get_nric()
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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

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
    session.pop('NRIC', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error500.html'), 500

###############This is where Benson's code ends###################################

####################This is where Isaac's code begins#######################################

# CUSTOMER SIDE
today = date.today()
@app.route('/createAppointment', methods=['GET', 'POST'])
def create_appointment():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

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
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']

        for key in customers_dict:
            customer = customers_dict.get(key)
            if customer.get_nric() == session['NRIC']: #check if the appointment is made by the user
                create_appointment_form.name_ment.data = customer.get_name()
                create_appointment_form.age_ment.data = customer.get_age()
                create_appointment_form.gender_ment.data = customer.get_gender()
                create_appointment_form.nric_ment.data = customer.get_nric()
                create_appointment_form.email_ment.data = customer.get_email()
                create_appointment_form.address_ment.data = customer.get_address()
                create_appointment_form.past_condition_ment.data = customer.get_condition()

        db.close()

        return render_template('createAppointment.html', form=create_appointment_form)

@app.route('/retrieveAppointments')
def retrieve_appointments():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    for key in appointments_dict:
        appointment = appointments_dict.get(key)
        if appointment.get_nric_ment() == session['NRIC']: #check if the appointment is made by the user
            if appointment.get_date_ment().strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d"):
                appointment.set_attendance_ment('Unattended')
                appointment.set_meeting_status_ment('Over')

    db['Appointments'] = appointments_dict
    db.close()

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
        if appointment.get_nric_ment() == session['NRIC']: #check if the appointment is made by the user
            if appointment.get_meeting_status_ment() != 'Over':
                appointments_list.append(appointment)

    appointments_list = sorted(appointments_list, key=lambda x: x.get_date_ment())

    return render_template('retrieveAppointments.html', count=len(appointments_list), appointments_list=appointments_list)

@app.route('/updateAppointment/<int:id>/', methods=['GET', 'POST'])
def update_appointment(id):
    if 'NRIC' not in session:
        return redirect(url_for('login'))

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

@app.route('/retrieveMissedAppointments')
def retrieve_missed_appointments():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    for key in appointments_dict:
        appointment = appointments_dict.get(key)
        if appointment.get_nric_ment() == session['NRIC']: #check if the appointment is made by the user
            if appointment.get_date_ment().strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d"):
                appointment.set_attendance_ment('Unattended')
                appointment.set_meeting_status_ment('Over')

    db['Appointments'] = appointments_dict
    db.close()

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
        if appointment.get_nric_ment() == session['NRIC']: #check if the appointment is made by the user
            if appointment.get_attendance_ment() == 'Unattended':
                appointments_list.append(appointment)

    appointments_list = sorted(appointments_list, key=lambda x: x.get_date_ment(), reverse=True)

    return render_template('retrieveMissedAppointments.html', count=len(appointments_list), appointments_list=appointments_list)

@app.route('/rescheduleAppointment/<int:id>/', methods=['GET', 'POST'])
def reschedule_appointment(id):
    if 'NRIC' not in session:
        return redirect(url_for('login'))

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

        return render_template('rescheduleAppointment.html', form=update_appointment_form)

# ADMIN SIDE
@app.route('/Admin_Homepage', methods=['GET', 'POST'])
def retrieve_appointments_admin():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

    appointments_dict = {}
    db = shelve.open('appointment.db', 'w')
    appointments_dict = db['Appointments']

    for key in appointments_dict:
        appointment = appointments_dict.get(key)
        if appointment.get_date_ment().strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d"):
            appointment.set_attendance_ment('Unattended')
            appointment.set_meeting_status_ment('Over')

    db['Appointments'] = appointments_dict
    db.close()

    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    doctor_filter_form = DoctorFilterForm(request.form)
    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)
        if appointment.get_meeting_status_ment() != 'Over':

            #Filtering by doctor
            if request.method == 'POST' and doctor_filter_form.validate():
                if doctor_filter_form.filterDoctor.data == 'All':
                    appointments_list.append(appointment)

                elif doctor_filter_form.filterDoctor.data == appointment.get_doctor_ment():
                    appointments_list.append(appointment)

            else:
                appointments_list.append(appointment)

    appointments_list = sorted(appointments_list, key=lambda x: x.get_date_ment())

    return render_template('Admin_Homepage.html', form=doctor_filter_form, count=len(appointments_list), appointments_list=appointments_list)

@app.route('/updateAppointmentAdmin/<int:id>/', methods=['GET', 'POST'])
def update_appointment_admin(id):
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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

@app.route('/retrievePastAppointmentsAdmin', methods=['GET','POST'])
def retrieve_past_appointments_admin():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    doctor_filter_form = DoctorFilterForm(request.form)
    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)

        if appointment.get_meeting_status_ment() == 'Over':

            #Filtering by doctor
            if request.method == 'POST' and doctor_filter_form.validate():
                if doctor_filter_form.filterDoctor.data == 'All':
                    appointments_list.append(appointment)

                elif doctor_filter_form.filterDoctor.data == appointment.get_doctor_ment():
                    appointments_list.append(appointment)

            else:
                appointments_list.append(appointment)

    appointments_list = sorted(appointments_list, key=lambda x: x.get_date_ment(), reverse=True)

    return render_template('retrievePastAppointmentsAdmin.html', form=doctor_filter_form, count=len(appointments_list), appointments_list=appointments_list)

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

@app.route('/retrieveUnattendedAppointmentsAdmin', methods=['GET', 'POST'])
def retrieve_unattended_appointments_admin():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

    appointments_dict = {}
    db = shelve.open('appointment.db', 'r')
    try:
        if 'Appointments' in db:
            appointments_dict = db['Appointments']
        else:
            db['Appointments'] = appointments_dict
    except:
        print('Error')

    doctor_filter_form = DoctorFilterForm(request.form)
    appointments_list = []
    for key in appointments_dict:
        appointment = appointments_dict.get(key)

        if appointment.get_attendance_ment() == 'Unattended':

            #Filtering by doctor
            if request.method == 'POST' and doctor_filter_form.validate():
                if doctor_filter_form.filterDoctor.data == 'All':
                    appointments_list.append(appointment)

                elif doctor_filter_form.filterDoctor.data == appointment.get_doctor_ment():
                    appointments_list.append(appointment)

            else:
                appointments_list.append(appointment)

    appointments_list = sorted(appointments_list, key=lambda x: x.get_date_ment(), reverse=True)

    return render_template('retrieveUnattendedAppointmentsAdmin.html', form=doctor_filter_form, count=len(appointments_list), appointments_list=appointments_list)

###############This is where Isaac's code ends###################################

####################This is where Jai's code begins#######################################

@app.route('/createFeedback', methods=['GET', 'POST'])
def create_feedback():
    if 'NRIC' not in session:
        return redirect(url_for('login'))

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

    if session["NRIC"] != 'ADMIN':
        return render_template('error404.html'), 404

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
    if 'NRIC' not in session:
        return redirect(url_for('login'))

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

###############This is where Jai's code ends###################################

if __name__ == '__main__':
    app.run()
