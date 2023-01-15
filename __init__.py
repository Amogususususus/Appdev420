from flask import Flask, render_template, request, redirect, url_for
from templates.forms import CreateSyrupForm
import shelve
import templates.Syrup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('alanhome.html')


@app.route('/contactUs')
def contact_us():
    return render_template('Contact.html')

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

            print("Error in retrieving Syrups from customer.db.")

        syrup = templates.Syrup.Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                                      Create_Syrup_form.Stock_Medication.data,
                                      Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data, Create_Syrup_form.Picture.data)

        syrups_dict[syrup.get_id()] = syrup
        db['Syrups'] = syrups_dict

        db.close()


    return render_template('Medication_Management.html', form=Create_Syrup_form)

@app.route('/retrieveSyrup', methods=['GET', 'POST'])
def retrieve_Syrup():
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

        if len(syrups_dict) == 0:
            syrup = templates.Syrup.Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                                    Create_Syrup_form.Stock_Medication.data,
                                    Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data, Create_Syrup_form.Picture.data,len(syrups_dict))

        else:
            last_object = syrups_list[-1]
            syrup = templates.Syrup.Syrup(Create_Syrup_form.Medication_name.data, Create_Syrup_form.Price_Medication.data,
                        Create_Syrup_form.Stock_Medication.data,
                        Create_Syrup_form.Size.data, Create_Syrup_form.Description_Medication.data, Create_Syrup_form.Picture.data, last_object.get_id())

        syrups_dict[syrup.get_id()] = syrup
        db['Syrups'] = syrups_dict

        return redirect (url_for('retrieve_Syrup'))
    return render_template('retrieveSyrup.html',count=len(syrups_list), syrups_list=syrups_list, form=Create_Syrup_form)

@app.route('/retrieveSyrup/<int:id>/', methods=['GET', 'POST'])
def update_Syrup(id):
    Update_Syrup_form = CreateSyrupForm(request.form)
    if request.method == 'POST' and Update_Syrup_form.validate():
        syrups_dict = {}
        db = shelve.open('Syrup.db', 'w')
        syrups_dict = db['Syrups']
        syrup = syrups_dict.get(id)
        syrup.set_name(Update_Syrup_form.Medication_name.data)
        syrup.set_price(Update_Syrup_form.Price_Medication.data)
        syrup.set_stock(Update_Syrup_form.Stock_Medication.data)
        syrup.set_Volume(Update_Syrup_form.Size.data)
        syrup.set_Picture(Update_Syrup_form.Picture.data)
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
        Update_Syrup_form.Picture.data = syrup.get_Picture()
        Update_Syrup_form.Description_Medication.data = syrup.get_Description()
        return render_template('retrieveSyrup.html', form=Update_Syrup_form)

@app.route('/delete_syrups/<int:id>', methods=['POST'])
def delete_syrup(id):
    syrups_dict = {}
    db = shelve.open('syrup.db', 'w')
    syrups_dict = db['Syrups']
    syrups_dict.pop(id)
    db['Syrups'] = syrups_dict

    return redirect(url_for('retrieve_Syrup'))

if __name__ == '__main__':
    app.run(debug=True)
