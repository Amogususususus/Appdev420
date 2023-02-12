from wtforms import StringField, TextAreaField, IntegerField, SubmitField, ValidationError, SelectField
from wtforms.validators import Optional, Length, DataRequired, NumberRange
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import DateField
from datetime import date

class orderform(FlaskForm):
    address = StringField(label=('Address:'), validators=[DataRequired(), Length(min=1, max=50, message='Name length must be between %(min)d and %(max)d characters')], render_kw={'placeholder' : 'Enter Address...'})
    name = StringField(label=('Name of Recipient:'), validators=[DataRequired(), Length(min=1, max=50, message='Name length must be between %(min)d and %(max)d characters')], render_kw={'placeholder' : 'Enter Name of recipient...'})
    submit = SubmitField(label=('Make an Order'))

class itemform(FlaskForm):
    quantity=IntegerField(label=('Quantity: '), validators=[DataRequired()], render_kw={'placeholder' : 'Quantity...'})
    submit=SubmitField(label=('Add to Cart'))

class FilterForm(FlaskForm):
    Filter=SelectField(label=("Filter by Lowest stock"), choices=[('unfiltered', ' Lowest Stock unfiltered '), ('filtered', ' Lowest Stock filtered ')], validators=[Optional()])
    submit=SubmitField(label=('Sort'))

class SearchForm(FlaskForm):
    searched=StringField(label=("Search"), validators=[DataRequired()], render_kw={'placeholder' : 'Search...'})
    submit=SubmitField(label=('Search'))

class Adding_Stock_Form(FlaskForm):
    Addition_Value = IntegerField("enter the amount you are adding")
    submit = SubmitField("Add")

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], message='File Type Not Allowed!')], render_kw={'placeholder' : 'Enter File...'})
    submitting = SubmitField("Upload File")

class CreateSyrupForm(FlaskForm):
    Medication_name = StringField(label=('Name of Medication:'), validators=[DataRequired(), Length(min=1, max=50, message='Name length must be between %(min)d and %(max)d characters')], render_kw={'placeholder' : 'Enter Name...'})
    Price_Medication = IntegerField(label=('Price of Medication:'), validators=[DataRequired()], render_kw={'placeholder' : 'Enter Price...'})
    Stock_Medication = IntegerField(label=('Stock of Medication:'), validators=[DataRequired(), NumberRange(min=30, max=1000, message='You are only allowed to set the Stock between%(min)d and %(max])d ')], render_kw={'placeholder' : 'Enter Stock...'})
    Size = StringField(label=('Size of Medication (per pack):'), validators=[DataRequired()], render_kw={'placeholder' : 'Enter Volume/weight of medication...'})
    Picture = TextAreaField('Please enter the name of the file with no spaces!', validators=[Optional()])
    Expiration = DateField('Date of Expiry for Current batch', format='%Y-%m-%d')
    Description_Medication = TextAreaField(label=('Description of Medication:'), validators=[DataRequired()], render_kw={'placeholder' : 'Enter Description...'})
    submit=SubmitField(label=('Submit'))

    def validate_Medication_name(self, Medication_name):
        excluded_chars = "*?!'^+%&/()=}][{$#"
        for char in self.Medication_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in Medication name.")

    def validate_Expiration(form, Expiration):
        today = date.today()
        if Expiration.data.strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d"):
            raise ValidationError('Select an expiration date that is not in the past.')

        elif Expiration.data.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            raise ValidationError('Select an expiration date that is not the current date.')

    def validate_Price_Medication(self, Price_Medication):
        if self.Price_Medication.data > 100000:
            raise ValidationError('Price is too high, did you accidentally add an extra digit?')
        if self.Price_Medication.data < 0:
            raise ValidationError('Price is too low, did you forget to add an extra digit?')

    def validate_Stock_Medication(self, Stock_Medication):
        if self.Stock_Medication.data > 10000:
            raise ValidationError('Stock is going over available space, did you accidentally add an extra digit?')
        if self.Stock_Medication.data < 0:
            raise ValidationError('Stock is too low, did you forget to add an extra digit?')

