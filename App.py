import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

app = Flask(__name__)
app.secret_key = 'jomak_secret_key_2026'

# Configuration de la base de données SQLite
DATABASE = 'jomak_service.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                specs TEXT NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL,
                image_url TEXT
            )
        ''')
        conn.commit()

# Initialisation de la BDD au démarrage
init_db()

@app.route('/')
def index():
    with get_db_connection() as conn:
        materials = conn.execute('SELECT * FROM materials').fetchall()
    return render_template('index.html', materials=materials)

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == 'jomak26':
        session['admin'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Code incorrect'})

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_material():
    if not session.get('admin'):
        return redirect(url_for('index'))
    
    mat_type = request.form.get('type')
    brand = request.form.get('brand')
    model = request.form.get('model')
    specs = request.form.get('specs')
    price = request.form.get('price')
    status = request.form.get('status')
    
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO materials (type, brand, model, specs, price, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (mat_type, brand, model, specs, price, status))
        conn.commit()
        
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_material(id):
    if not session.get('admin'):
        return redirect(url_for('index'))
    
    with get_db_connection() as conn:
        conn.execute('DELETE FROM materials WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('index'))

# --- MODULE IA INTÉGRÉ ---
@app.route('/api/ai-analysis', methods=['POST'])
def ai_analysis():
    data = request.json
    brand = data.get('brand', '')
    model = data.get('model', '')
    specs = data.get('specs', '')
    
    # Simulation locale d'un argumentaire IA pertinent pour la maintenance et la vente
    argumentaire = (
        f"Analyse Technique Optimisée pour le {brand} {model}.\n\n"
        f"Points forts : Ce matériel configuré en '{specs}' offre une excellente gestion thermique "
        f"et une durabilité matérielle éprouvée, idéale pour les professionnels. "
        f"Performances fluides garanties pour les applications bureautiques avancées et le développement."
    )
    return jsonify({'analysis': argumentaire})

if __name__ == '__main__':
    # Utilisation du port fourni par Render ou 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
