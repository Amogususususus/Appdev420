from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, ValidationError
from wtforms.fields import EmailField, IntegerField, PasswordField
import shelve

class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    condition = TextAreaField('Pre-existing Medical Conditions', [validators.Optional()])

class CreateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    age = IntegerField('Age', [validators.NumberRange(min=1,max=120), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    condition = TextAreaField('Pre-existing Medical Conditions (optional)', [validators.Optional()])
    password = StringField('Password', [validators.Length(min=8, max=16), validators.DataRequired()])
    nric =StringField('NRIC', [validators.Length(min=9, max=9)])

    def validate_nric(form, field):
        if field.data[0].upper() != "S" and field.data[0].upper() != "T":
            raise ValidationError('First character has to be S or T.')

        elif field.data[1:8].isnumeric() == False:
            raise ValidationError('Characters 2 to 7 has to be numerical digits.')

        elif field.data[-1].isalpha() == False:
            raise ValidationError('Last character has to be a letter.')

    def validate_name(form,field):
        if field.data.replace(" ","").isalpha() == False:
            raise ValidationError('Name cannot contain numbers')

class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=16), validators.DataRequired()])


    def validate_password(self,password):
        email_password_list =[]
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        for key in customers_dict:
            customer = customers_dict.get(key)
            customer_pair = [customer.get_email(),customer.get_password()]
            email_password_list.append(customer_pair)

        id = None
        for n in email_password_list:
            if self.email.data == n[0]:
                id = n

        if id is not None:
            if self.password.data != id[1]:
                raise ValidationError('Incorrect Email or Password')






