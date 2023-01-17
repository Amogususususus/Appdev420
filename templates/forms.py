from wtforms import StringField, TextAreaField, validators, IntegerField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
class CreateSyrupForm(FlaskForm):
    Medication_name = StringField('Name of Medication', [validators.Length(min=1, max=150), validators.DataRequired()])
    Price_Medication = IntegerField('Price of Medication', [ validators.DataRequired()])
    Stock_Medication = IntegerField('Stock of Medication', [ validators.DataRequired()])
    Size = StringField('Volume of Medication', [ validators.DataRequired()])
    Picture = FileField('Picture of Medication', validators=[FileAllowed(['jpg'], message='File Not Allowed')])
    Description_Medication = TextAreaField('Remarks', [validators.DataRequired()])


