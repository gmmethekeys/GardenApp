"""Create form logic."""
from wtforms import (Form,
                     StringField,
                     PasswordField,
                     SubmitField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                Optional)


class SignupForm(Form):
    """User Signup Form."""

    name = StringField('Name',
                       validators=[DataRequired(message=('Please enter in a name.'))])

    email = StringField('Email',
                        validators=[Length(min=6, message=('Please enter a valid email address.')),
                                    Email(message=('Please enter a valid email address.')),
                                    DataRequired(message=('Please enter a valid email address.'))])

    password = PasswordField('Password',
                             validators=[DataRequired(message='Please enter a password.'),
                                         Length(min=6, message=('Please select a stronger password.')),
                                         EqualTo('confirm', message='Passwords must match')])

    confirm = PasswordField('Confirm Your Password',)

    website = StringField('Website',
                          validators=[Optional()])

    submit = SubmitField('Register')


class LoginForm(Form):
    """User Login Form."""

    email = StringField('Email', validators=[DataRequired('Please enter a valid email address.'),
                                             Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired('Uhh, your password tho?')])
    submit = SubmitField('Log In')


class CreatePlantForm(Form):
    """Plant Creation Form."""

    plantName = StringField('plantName',
                            validators=[DataRequired('Please enter a plant name.'),
                                        Length(min=1, message=('Please enter a plant name that is longer.'))])

    plantType = StringField('plantType',
                            validators=[DataRequired(message=('Please enter a Plant Type.'))])

    plantThirst = StringField('plantThirst',
                              validators=[DataRequired(message=('Please enter a thirst value between 1-10.'))])

    sensorID = StringField('sensorID',
                           validators=[DataRequired(message=('Please enter the sensor ID, enter 555 for default.'))])

    submit = SubmitField('Submit')

class DeletePlantForm(Form):
    """Plant Deletion Form"""

    plantName1 = StringField('plantName',
                            validators=[DataRequired('Please enter a plant name you want to delete.'),
                                        Length(min=1, message=('Pleae enter a plant name that is longer.'))])

    delete = SubmitField('Delete')