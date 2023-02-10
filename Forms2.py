from wtforms import Form, validators, ValidationError
from wtforms.fields import EmailField, DateField, StringField, TextAreaField, RadioField
from datetime import date

class CreateFeedbackForm(Form):
    date = DateField('Date', [validators.DataRequired()], default=date.today(), render_kw={'readonly': True})
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=2, max=150)])
    email = StringField('Email')
    typeqn = RadioField('Type of Feedback', choices=[('C', 'Consultation'), ('M', 'Medication'), ('O', 'Others')])
    qn1 = TextAreaField('How was your experience with us?')
    qn2 = TextAreaField('How could we improve?', [validators.DataRequired()])

    def validate_date(form, field):
        today = date.today()
        if field.data.strftime('%Y-%m-%d') < today.strftime('%Y-%m-%d'):
            raise ValidationError("Select a date that's not in the past")


    def validate_email(form, field):
        if '@' not in field.data:
            raise ValidationError("Please make sure your email contains '@'")
        elif '.com' not in field.data:
            raise ValidationError("Please make sure your email contains '.com' at the end")



