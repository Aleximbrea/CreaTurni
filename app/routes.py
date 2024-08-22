from app import app
from flask import render_template, url_for, redirect
from app.forms import AddEmployee
from app import conn, cur

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/employees")
def employees():
    return render_template('employees.html')

@app.route("/add_employee", methods=['POST', 'GET'])
def add_employee():
    form = AddEmployee()
    form.set_choices()
    if form.validate_on_submit():
        # Getting values from form
        nominativo = form.nominativo.data
        id_ruolo = form.ruolo.data
        # Inserting new row in the vigilante table
        query = f"INSERT INTO vigilanti (nominativo, id_ruolo) VALUES ('{nominativo}', {id_ruolo})"
        cur.execute(query)
        conn.commit()
        
        # Getting vigilante's id to update preferences table
        query = f"SELECT id FROM vigilanti WHERE nominativo = '{nominativo}'"
        cur.execute(query)
        id_vigilante = cur.fetchone()[0]


        # Inserting preferences into preference table
        query = f"INSERT INTO preferenze (id_vigilante, ore_lavoro, piu_turni, inizio, fine, riposi) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (id_vigilante, form.ore.data, form.piu_turni.data, form.inizio.data, form.fine.data, form.riposi.data))
        conn.commit()

        return redirect( url_for('employees'))
    else:
        print(print(form.errors))
    return render_template('add_employee.html', form=form)
