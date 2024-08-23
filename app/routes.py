from app import app
from flask import render_template, url_for, redirect, request, jsonify
from app.forms import AddEmployee
from app import conn, cur

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/employees", methods=['POST', 'GET'])
def employees():

    form = AddEmployee()
    form.set_choices()

    # POST Method

    if request.method == 'POST':
        # Making sure name and ruolo are validated
        if form.validate_on_submit():
            # Getting values from form
            nominativo = form.nominativo.data.upper()
            id_ruolo = form.ruolo.data
            id_vigilante = int(form.hidden_id.data)
            # Updating vigilanti's table
            query = f"UPDATE vigilanti SET nominativo='{nominativo}', id_ruolo={id_ruolo} WHERE id={id_vigilante}"
            cur.execute(query)
            conn.commit()

        # Updating preferences
        piu_turni = True if request.form.get('piu_turni') == 'y' else False
        inizio = f'{request.form.get("inizio")}' if request.form.get("inizio") else None
        fine = f'{request.form.get("fine")}' if request.form.get("fine") else None
        riposi = int(request.form.get('riposi')) if request.form.get('riposi') else None
        ore = int(request.form.get('ore')) if request.form.get('ore') else None

        query = f"UPDATE preferenze SET ore_lavoro = %s, piu_turni = %s, inizio = %s, fine = %s, riposi = %s WHERE id_vigilante = %s"
        cur.execute(query, (ore ,piu_turni, inizio,  fine, riposi, request.form.get('hidden_id')))
        conn.commit()


    # GET Method
    requested_name = request.args.get('nominativo')

    if requested_name:
        query = f"SELECT id, nominativo, id_ruolo FROM vigilanti WHERE nominativo='{requested_name.upper()}'"
        cur.execute(query)
        vigilanti = cur.fetchall()
        if vigilanti:
            query = f"SELECT id, ruolo FROM ruoli WHERE id={vigilanti[0][2]}"
            cur.execute(query)
            ruoli = cur.fetchall()
        else:
            ruoli = None
    else:
        # Query to get all roles
        query = "SELECT id, ruolo FROM ruoli"
        cur.execute(query)
        ruoli = cur.fetchall()
        
        # Query to get all vigilantes with their role
        query = "SELECT id, nominativo, id_ruolo FROM vigilanti"
        cur.execute(query)
        vigilanti = cur.fetchall()
    return render_template('employees.html', ruoli=ruoli, vigilanti=vigilanti, form=form)

@app.route("/add_employee", methods=['POST', 'GET'])
def add_employee():
    form = AddEmployee()
    form.set_choices()
    if form.validate_on_submit():
        # Getting values from form
        nominativo = form.nominativo.data
        nominativo = nominativo.upper()
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
        print(form.errors)
    return render_template('add_employee.html', form=form)

@app.route("/get_vigilante_preferences", methods=['POST'])
def get_vigilante_preferences():

    data = request.get_json()
    vigilante_id = int(data.get('id'))

    # Query to get preferences from id
    query = f'SELECT * FROM preferenze WHERE id_vigilante = {vigilante_id}'
    cur.execute(query)
    pref = cur.fetchone()
    pref = list(pref)
    pref[4] = pref[4].strftime('%H:%M') if pref[4] else pref[4]
    pref[5] = pref[5].strftime('%H:%M') if pref[5] else pref[5]
    return jsonify(pref)

@app.route('/delete_vigilante', methods=['POST'])
def delete_vigilante():
    data = request.get_json()
    id = int(data.get('id'))

    try:
        # First i delete preferences
        query = f'DELETE FROM preferenze WHERE id_vigilante={id}'
        cur.execute(query)
        conn.commit()
        # Then i delete the vigilante
        query = f'DELETE FROM vigilanti WHERE id={id}'
        cur.execute(query)
        conn.commit()
        return jsonify(True)
    except Exception as e:
        return jsonify(False)
