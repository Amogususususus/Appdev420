from wtforms import Form, StringField, TextAreaField, validators, IntegerField, FileField
class CreateSyrupForm(Form):
    Medication_name = StringField('Name of Medication', [validators.Length(min=1, max=150), validators.DataRequired()])
    Price_Medication = IntegerField('Price of Medication', [ validators.DataRequired()])
    Stock_Medication = IntegerField('Stock of Medication', [ validators.DataRequired()])
    Size = StringField('Volume of Medication', [ validators.DataRequired()])
    Picture = FileField('Picture of Medication', [ validators.DataRequired()])
    Description_Medication = TextAreaField('Remarks', [validators.DataRequired()])


