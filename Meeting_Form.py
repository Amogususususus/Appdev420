from wtforms import Form, StringField, IntegerField, SelectField, TextAreaField, validators, ValidationError
from wtforms.fields import EmailField, DateField
from datetime import date

class AppointmentForm(Form):
    name_ment = StringField('Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    age_ment = IntegerField('Age', [validators.NumberRange(min=1, max=120), validators.DataRequired()])
    gender_ment = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    nric_ment = StringField('NRIC', [validators.Length(min=9, max=9), validators.DataRequired()])
    email_ment = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address_ment = TextAreaField('Address', [validators.length(min=5, max=200), validators.DataRequired()])
    remarks_ment = TextAreaField('Remarks', [validators.length(min=3, max=120), validators.Optional()])
    past_condition_ment = TextAreaField('Pre-Existing Medical Conditions', [validators.Optional()])
    doctor_ment = SelectField('Doctor', [validators.DataRequired()], choices=[('', 'Select'), ('Dr. Ong', 'Dr. Ong'), ('Dr. Lim', 'Dr. Lim')], default='')
    date_ment = DateField('Date of Appointment', format='%Y-%m-%d')
    time_ment = SelectField('Time (in hours)', [validators.DataRequired()], choices=[('', 'Select'),
                                                                                     ('9am', '0900'),
                                                                                     ('10am', '1000'),
                                                                                     ('11am', '1100'),
                                                                                     ('12pm', '1200'),
                                                                                     ('1pm', '1300'),
                                                                                     ('2pm', '1400'),
                                                                                     ('3pm', '1500'),
                                                                                     ('4pm', '1600'),
                                                                                     ('5pm', '1700'),
                                                                                     ('6pm', '1800'),
                                                                                     ('7pm', '1900'),
                                                                                     ('8pm', '2000'), ], default='')

    def validate_name_ment(form, field):
        if field.data.isalpha() == False:
            raise ValidationError('Enter a name using letters.')

    def validate_nric_ment(form, field):
        if field.data[0].upper() != "S" and field.data[0].upper() != "T":
            raise ValidationError('First character has to be S or T.')

        elif field.data[1:8].isnumeric() == False:
            raise ValidationError('Characters 2 to 7 has to be numerical digits.')

        elif field.data[-1].isalpha() == False:
            raise ValidationError('Last character has to be a letter.')

    def validate_date_ment(form, field):
        today = date.today()
        if field.data.strftime("%Y-%m-%d") < today.strftime("%Y-%m-%d"):
            raise ValidationError('Select an appointment date that is not in the past.')

        elif field.data.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            raise ValidationError('Select an appointment date that is not the current date.')
