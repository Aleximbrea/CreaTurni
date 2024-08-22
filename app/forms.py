from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired

class AddEmployee(Form):
    nominativo = StringField('nominativo', validators=[
        DataRequired("Inserire nominativo")
    ])