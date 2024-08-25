from app import app
from flask import render_template, url_for, redirect, request, jsonify
from app.forms import AddEmployee, AddPlace
from app import conn, cur
from datetime import datetime
import json
from app.functions import dictionary_query

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/appalti', methods=['POST','GET'])
def appalti():
    
    form = AddPlace()

    search_appalto = request.args.get('appalto')

    # POST
    if form.validate_on_submit():
        print(form.nome.data, form.inizio.data, form.fine.data, form.hidden_id.data)
        query = f'UPDATE appalti SET nome=%s, inizio=%s, fine=%s WHERE id=%s'
        cur.execute(query, (form.nome.data, form.inizio.data, form.fine.data, form.hidden_id.data))
        conn.commit()
    else:
        print(form.inizio.data, form.fine.data, form.hidden_id.data)
        query = f'UPDATE appalti SET inizio=%s, fine=%s WHERE id=%s'
        cur.execute(query, (form.inizio.data, form.fine.data, form.hidden_id.data))
        conn.commit()


    query = f'SELECT id, nome FROM appalti ORDER BY nome' if  not search_appalto else f"SELECT id, nome FROM appalti WHERE LOWER(nome) = LOWER('{search_appalto}');"
    cur.execute(query)
    appalti = cur.fetchall()

    return render_template('appalti.html', appalti=appalti, form=form)

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

        # Updating assegnazioni

        array = json.loads(form.hidden_array.data)
        print(array)
        for id in array:
            query = f'DELETE FROM assegnazioni WHERE id = {id}'
            cur.execute(query)
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
        array = json.loads(form.hidden_array.data)
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

        # Inserting assignments
        if array:
            for assegn in array:
                query = f'INSERT INTO assegnazioni (id_vigilante, id_appalto) VALUES (%s, %s)'
                cur.execute(query, (id_vigilante, int(assegn)))


        # Inserting preferences into preference table
        query = f"INSERT INTO preferenze (id_vigilante, ore_lavoro, piu_turni, inizio, fine, riposi) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (id_vigilante, form.ore.data, form.piu_turni.data, form.inizio.data, form.fine.data, form.riposi.data))
        conn.commit()

        return redirect( url_for('employees'))
    else:
        print(form.errors)
    return render_template('add_employee.html', form=form)

@app.route("/add_appalto", methods=['GET', 'POST'])
def add_appalto():
    form = AddPlace()
    if form.validate_on_submit():
        query = f"INSERT INTO appalti (nome, inizio, fine) VALUES (%s, %s, %s)"
        cur.execute(query, (form.nome.data, form.inizio.data, form.fine.data))
        conn.commit()
        return redirect(url_for('appalti'))

    return render_template('add_appalto.html', form=form)

@app.route("/get_vigilante_preferences", methods=['POST'])
def get_vigilante_preferences():

    data = request.get_json()
    vigilante_id = int(data.get('id'))

    results = []
    # Queries
    queries = [
        f'SELECT * FROM preferenze WHERE id_vigilante = {vigilante_id}',
        f'SELECT assegnazioni.id, appalti.nome FROM assegnazioni INNER JOIN appalti ON assegnazioni.id_appalto = appalti.id WHERE id_vigilante = {vigilante_id}'
    ]
    for query in queries:
        cur.execute(query)
        data = dictionary_query(cur, query)
        results.append(data)

    # Formatting time objects
    results[0][0]['inizio'] = results[0][0]['inizio'].strftime('%H:%M') if results[0][0]['inizio'] else results[0][0]['inizio']
    results[0][0]['fine'] = results[0][0]['fine'].strftime('%H:%M') if results[0][0]['fine'] else results[0][0]['fine']
    return jsonify(results)

@app.route("/get_appalto_info", methods=['POST'])
def get_appalto_info():

    data = request.get_json()
    id = int(data.get('id'))

    query = f'SELECT * FROM appalti WHERE id = {id}'
    cur.execute(query)
    info = list(cur.fetchone())

    # Formatting dates
    info[2] = info[2].strftime('%Y:%m:%d').replace(':', '-') if info[2] else None
    info[3] = info[3].strftime('%Y:%m:%d').replace(':', '-') if info[3] else None

    return jsonify(info)

@app.route('/delete_appalto', methods=['POST'])
def delete_appalto():
    data = request.get_json()
    id = int(data.get('id'))

    # Deleting all relations 
    queries = [
        f'DELETE FROM orari WHERE id_appalto = {id}',
        f'DELETE FROM assegnazioni WHERE id_appalto = {id}',
        f'DELETE FROM servizi WHERE id_appalto = {id}',
        f'DELETE FROM appalti WHERE id = {id}'
    ]

    try:
        for query in queries:
            cur.execute(query)
            conn.commit()
        return jsonify(True)
    except Exception as e:
        return jsonify(False)

@app.route('/delete_vigilante', methods=['POST'])
def delete_vigilante():
    data = request.get_json()
    id = int(data.get('id'))

    try:
        queries = [f'DELETE FROM preferenze WHERE id_vigilante={id}', 
                   f'DELETE FROM assegnazioni WHERE id_vigilante={id}',
                    f'DELETE FROM vigilanti WHERE id={id}'
                   ]
        for query in queries:
            cur.execute(query)
            conn.commit()
        return jsonify(True)
    except Exception as e:
        return jsonify(False)

