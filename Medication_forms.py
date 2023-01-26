from wtforms import StringField, TextAreaField, IntegerField, SubmitField, ValidationError
from wtforms.validators import Optional, Length, DataRequired, NumberRange
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from datetime import date
class CreateSyrupForm(FlaskForm):
    Medication_name = StringField(label=('Name of Medication:'), validators=[DataRequired(), Length(min=1, max=50, message='Name length must be between %(min)d and %(max)d characters')])
    Price_Medication = IntegerField(label=('Price of Medication:'), validators=[DataRequired()])
    Stock_Medication = IntegerField(label=('Stock of Medication:'), validators=[DataRequired(), NumberRange(min=30, max=1000, message='You are only allowed to set the Stock between%(min)d and %(max])d ')])
    Size = StringField(label=('Size of Medication (per pack):'), validators=[DataRequired()])
    Picture = TextAreaField('Please enter the name of the file with no spaces!', validators=[Optional()])
    Expiration = DateField('Date of Expiry for Current batch', format='%Y-%m-%d')
    Description_Medication = TextAreaField(label=('Description of Medication:'), validators=[DataRequired()])
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


