import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "chiave_segreta_super_sicura"

# upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = MongoClient('mongodb://localhost:27017/')
db = client['arredamento_db']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#     ROTTE PAGINE WEB


@app.route('/')
def home():
    prodotti = list(db.prodotti.find())
    return render_template('home.html', prodotti=prodotti)

@app.route('/catalogo')
def catalogo():
    categoria = request.args.get('categoria')
    min_p = request.args.get('min_prezzo')
    max_p = request.args.get('max_prezzo')
    search_query = request.args.get('q')

    filtro_db = {}
    if search_query:
        filtro_db['nome'] = {'$regex': search_query, '$options': 'i'}
    if categoria and categoria != "Tutte":
        filtro_db['categoria'] = categoria
    if min_p or max_p:
        filtro_db['prezzo'] = {}
        if min_p:
            try: filtro_db['prezzo']['$gte'] = float(min_p)
            except: pass
        if max_p:
            try: filtro_db['prezzo']['$lte'] = float(max_p)
            except: pass

    prodotti = list(db.prodotti.find(filtro_db))
    for p in prodotti:
        p['_id'] = str(p['_id'])
        
    return render_template('catalogo.html', prodotti=prodotti, cat_selezionata=categoria, min_p=min_p, max_p=max_p, q=search_query)

@app.route('/prodotto/<id_prodotto>')
def pagina_prodotto(id_prodotto):
    try:
        prodotto = db.prodotti.find_one({"_id": ObjectId(id_prodotto)})
        if prodotto:
            prodotto['_id'] = str(prodotto['_id'])
            return render_template('prodotto.html', p=prodotto)
        else:
            return "Prodotto non trovato", 404
    except:
        return "ID Prodotto non valido", 400

@app.route('/checkout')
def checkout():
    if 'utente_nome' not in session: return redirect(url_for('home'))
    utente = db.utenti.find_one({"nome": session['utente_nome']})
    return render_template('checkout.html', u=utente)

@app.route('/account')
def account():
    if 'utente_nome' not in session: return redirect(url_for('home'))
    utente = db.utenti.find_one({"nome": session['utente_nome']})
    lista_ordini = list(db.ordini.find({"utente": session['utente_nome']}).sort("data_ordine", -1))
    return render_template('account.html', u=utente, ordini=lista_ordini)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

#area admin

@app.route('/admin')
def admin_dashboard():
    if 'utente_nome' not in session or session.get('ruolo') != 'admin':
        return redirect(url_for('home'))
    
    prodotti = list(db.prodotti.find())
    ordini = list(db.ordini.find().sort("data_ordine", -1))
    
    
    prodotti_map = {}
    for p in prodotti:
        p['_id'] = str(p['_id'])
        prodotti_map[str(p['_id'])] = p
        
    for o in ordini:
        o['_id'] = str(o['_id'])
    
    # statistics
    totale_incassi = sum(o['totale'] for o in ordini)
    numero_ordini = len(ordini)
    totale_spese_spedizione = numero_ordini * 15.0 
    guadagno_netto = totale_incassi - totale_spese_spedizione

    # staistics for category
    cat_stats = {
        'Soggiorno': {'incassi': 0, 'pezzi': 0},
        'Cucina':    {'incassi': 0, 'pezzi': 0},
        'Camera':    {'incassi': 0, 'pezzi': 0},
        'Bagno':     {'incassi': 0, 'pezzi': 0}
    }

    for o in ordini:
        for item in o['prodotti']:
            pid = item['id']
          
            cat_corrente = 'Altro'
            if pid in prodotti_map:
                cat_corrente = prodotti_map[pid].get('categoria', 'Altro')
            
            if cat_corrente in cat_stats:
                prezzo_tot = item['prezzo'] * item['quantita']
                cat_stats[cat_corrente]['incassi'] += prezzo_tot
                cat_stats[cat_corrente]['pezzi'] += item['quantita']
    
    COSTO_GESTIONE_PEZZO = 5.0
    stats_finali_cat = []
    for cat, dati in cat_stats.items():
        spese = dati['pezzi'] * COSTO_GESTIONE_PEZZO
        utile = dati['incassi'] - spese
        stats_finali_cat.append({
            'nome': cat,
            'incassi': dati['incassi'],
            'pezzi': dati['pezzi'],
            'spese': spese,
            'utile': utile
        })

    return render_template('admin_dashboard.html', 
                           prodotti=prodotti, 
                           ordini=ordini,
                           stats={ 
                               "incassi": totale_incassi, 
                               "ordini": numero_ordini, 
                               "spese_sped": totale_spese_spedizione, 
                               "netto": guadagno_netto 
                           },
                           cat_stats=stats_finali_cat)


# api admin


@app.route('/api/nuovo_prodotto', methods=['POST'])
def nuovo_prodotto():
    if session.get('ruolo') != 'admin': return jsonify({"success": False, "errore": "Non autorizzato"})
    
    nome = request.form.get('nome')
    prezzo = request.form.get('prezzo')
    categoria = request.form.get('categoria')
    misure = request.form.get('misure')
    materiali = request.form.get('materiali')
    descrizione = request.form.get('descrizione')
    file = request.files.get('immagine')

    if not file or not allowed_file(file.filename):
        return jsonify({"success": False, "errore": "Immagine mancante o non valida"})

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{filename}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    percorso_img = f"/static/uploads/{filename}"

    nuovo = {
        "nome": nome,
        "prezzo": float(prezzo),
        "categoria": categoria,
        "immagine": percorso_img,
        "misure": misure,
        "materiali": materiali,
        "descrizione": descrizione
    }

    db.prodotti.insert_one(nuovo)
    return jsonify({"success": True})

@app.route('/api/modifica_prodotto', methods=['POST'])
def modifica_prodotto():
    if session.get('ruolo') != 'admin': return jsonify({"success": False})

    prod_id = request.form.get('id')
    
    update_data = {
        "nome": request.form.get('nome'),
        "prezzo": float(request.form.get('prezzo')),
        "categoria": request.form.get('categoria'),
        "misure": request.form.get('misure'),
        "materiali": request.form.get('materiali'),
        "descrizione": request.form.get('descrizione')
    }

    file = request.files.get('immagine')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        update_data["immagine"] = f"/static/uploads/{filename}"

    db.prodotti.update_one({"_id": ObjectId(prod_id)}, {"$set": update_data})
    return jsonify({"success": True})

@app.route('/api/elimina_prodotto', methods=['POST'])
def elimina_prodotto():
    if session.get('ruolo') != 'admin': return jsonify({"success": False})
    dati = request.json
    db.prodotti.delete_one({"_id": ObjectId(dati.get('id'))})
    return jsonify({"success": True})


# api users


@app.route('/api/registra', methods=['POST'])
def api_registra():
    dati = request.json
    nome = dati.get('nome')
    email = dati.get('email')
    password = dati.get('password')
    
    if db.utenti.find_one({"email": email}):
        return jsonify({"success": False, "errore": "Email già esistente"})
    
    hashed_password = generate_password_hash(password)
    db.utenti.insert_one({
        "nome": nome,
        "email": email,
        "password": hashed_password,
        "ruolo": "cliente",
        "indirizzi": [],
        "metodi_pagamento": [],
        "telefono": ""
    })
    
    session['utente_nome'] = nome
    session['ruolo'] = 'cliente'
    return jsonify({"success": True})

@app.route('/api/login', methods=['POST'])
def api_login():
    dati = request.json
    email = dati.get('email')
    password = dati.get('password')
    
    utente = db.utenti.find_one({"email": email})
    
    if utente and check_password_hash(utente['password'], password):
        session['utente_nome'] = utente['nome']
        session['ruolo'] = utente.get('ruolo', 'cliente') 
        return jsonify({
            "success": True, 
            "ruolo": session['ruolo']
        })
    else:
        return jsonify({"success": False, "errore": "Credenziali errate"})

@app.route('/api/salva_ordine', methods=['POST'])
def salva_ordine():
    if 'utente_nome' not in session:
        return jsonify({"success": False, "errore": "Login richiesto"})
    
    dati = request.json
    nuovo_ordine = {
        "utente": session['utente_nome'],
        "prodotti": dati.get('prodotti'),
        "totale": dati.get('totale'),
        "indirizzo": dati.get('indirizzo'),
        "metodo": dati.get('metodo'),
        "data_ordine": datetime.now(),
        "stato": "In lavorazione"
    }
    db.ordini.insert_one(nuovo_ordine)
    return jsonify({"success": True})

# Account Management API
@app.route('/api/aggiorna_account', methods=['POST'])
def aggiorna_account():
    if 'utente_nome' not in session: return jsonify({"success": False})
    dati = request.json
    update_data = { "email": dati.get('email'), "telefono": dati.get('telefono') }
    if dati.get('password'): update_data["password"] = generate_password_hash(dati.get('password'))
    db.utenti.update_one({"nome": session['utente_nome']}, {"$set": update_data})
    return jsonify({"success": True})

@app.route('/api/aggiungi_indirizzo', methods=['POST'])
def aggiungi_indirizzo():
    if 'utente_nome' not in session: return jsonify({"success": False})
    db.utenti.update_one({"nome": session['utente_nome']}, {"$push": {"indirizzi": request.json}})
    return jsonify({"success": True})

@app.route('/api/rimuovi_indirizzo', methods=['POST'])
def rimuovi_indirizzo():
    if 'utente_nome' not in session: return jsonify({"success": False})
    idx = request.json.get('indice')
    db.utenti.update_one({"nome": session['utente_nome']}, {"$unset": {f"indirizzi.{idx}": 1}})
    db.utenti.update_one({"nome": session['utente_nome']}, {"$pull": {"indirizzi": None}})
    return jsonify({"success": True})

@app.route('/api/aggiungi_carta', methods=['POST'])
def aggiungi_carta():
    if 'utente_nome' not in session: return jsonify({"success": False})
    db.utenti.update_one({"nome": session['utente_nome']}, {"$push": {"metodi_pagamento": request.json}})
    return jsonify({"success": True})

@app.route('/api/rimuovi_carta', methods=['POST'])
def rimuovi_carta():
    if 'utente_nome' not in session: return jsonify({"success": False})
    idx = request.json.get('indice')
    db.utenti.update_one({"nome": session['utente_nome']}, {"$unset": {f"metodi_pagamento.{idx}": 1}})
    db.utenti.update_one({"nome": session['utente_nome']}, {"$pull": {"metodi_pagamento": None}})
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)