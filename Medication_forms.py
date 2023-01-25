from wtforms import StringField, TextAreaField, IntegerField, SubmitField, FloatField, ValidationError
from wtforms.validators import Optional, Length, DataRequired, NumberRange
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from datetime import date
class CreateSyrupForm(FlaskForm):
    Medication_name = StringField(label=('Name of Medication:'), validators=[DataRequired(), Length(min=1, max=50, message='Name length must be between %(min)d and %(max)d characters')])
    Price_Medication = IntegerField(label=('Price of Medication:'), validators=[DataRequired(), NumberRange(min=1, max=1000, message='You are only allowed to set the price between%(min)d and %(max)d $')])
    Stock_Medication = IntegerField(label=('Stock of Medication:'), validators=[DataRequired(), NumberRange(min=1, max=1000, message='You are only allowed to set the Stock between%(min)d and %(max])d ')])
    Size = StringField(label=('Size of Medication (per pack):'), validators=[DataRequired()])
    Picture = TextAreaField('Please enter the name of the file with no spaces!', validators=[Optional()])
    Expiration = DateField('Date of Expiry for Current batch', format='%Y-%m-%d')
    Description_Medication = TextAreaField(label=('Description of Medication:'), validators=[DataRequired()])
    submit=SubmitField(label=('Submit'))

    def validate_date(form, field):
        today = date.today()
        if field.data.strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d"):
            raise ValidationError('Please select a date that is not in the past.')

        elif field.data.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            raise ValidationError('Please select a date that is not the current date.')

