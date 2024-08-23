from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField, IntegerField, BooleanField, TimeField, HiddenField
from wtforms.validators import DataRequired, Optional, ValidationError
from app import conn, cur

def user_exists(form, field):
    # Getting a list of every nominativo
    query = "SELECT nominativo FROM vigilanti"
    cur.execute(query)
    nominativi = [row[0].upper() for row in cur.fetchall()]

    if field.data.upper() in nominativi:
        raise ValidationError('Nominativo già esistente')


class AddEmployee(FlaskForm):
    hidden_id = HiddenField('Hidden ID')
    nominativo = StringField('Nominativo', validators=[
        DataRequired("Inserire nominativo"), user_exists
    ])
    ruolo = SelectField('Ruolo', coerce=int, validators=[
        DataRequired("Scegli un ruolo")
    ])
    ore =IntegerField('Ore', validators=[Optional()])
    piu_turni = BooleanField('Più turni')
    riposi = IntegerField('Riposi', validators=[Optional()])
    inizio = TimeField('Inizio', validators=[Optional()])
    fine = TimeField('Fine', validators=[Optional()])

    def set_choices(self):
        cur.execute('SELECT id, ruolo FROM ruoli')
        choices = cur.fetchall()
        self.ruolo.choices = [(choice[0], choice[1]) for choice in choices]
