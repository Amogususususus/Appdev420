from wtforms import StringField, TextAreaField, validators, IntegerField, Form
from wtforms.validators import Optional
class CreateSyrupForm(Form):
    Medication_name = StringField('Name of Medication', [validators.Length(min=1, max=150), validators.DataRequired()])
    Price_Medication = IntegerField('Price of Medication', [validators.DataRequired()])
    Stock_Medication = IntegerField('Stock of Medication', [validators.DataRequired()])
    Size = StringField('Volume of Medication', [validators.DataRequired()])
    Picture = TextAreaField('Please enter the name of the file with no spaces!', validators=[Optional()])
    Description_Medication = TextAreaField('Remarks', [validators.DataRequired()])
