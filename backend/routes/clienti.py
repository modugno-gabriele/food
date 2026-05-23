from flask import Blueprint, jsonify, request
from db import get_connection

clienti_bp = Blueprint('clienti', __name__)

# ── GET /api/clienti  ────────────────────────────────────────────────
@clienti_bp.route('/', methods=['GET'])
def lista_clienti():
    cerca = request.args.get('cerca', '')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM clienti
                WHERE nome LIKE %s OR cognome LIKE %s OR email LIKE %s
                ORDER BY cognome, nome
            """, (f'%{cerca}%', f'%{cerca}%', f'%{cerca}%'))
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET /api/clienti/<id>  (dettaglio + storico ordini) ──────────────
@clienti_bp.route('/<int:id>', methods=['GET'])
def dettaglio_cliente(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM clienti WHERE id_cliente = %s", (id,))
            cliente = cur.fetchone()
            if not cliente:
                conn.close()
                return jsonify({'error': 'Cliente non trovato'}), 404

            cur.execute("""
                SELECT o.id_ordine, o.data_ora, o.stato, o.totale,
                       f.nome AS fattorino
                FROM ordine o
                LEFT JOIN fattorino f ON o.id_fattorino = f.id_fattorino
                WHERE o.id_cliente = %s
                ORDER BY o.data_ora DESC
            """, (id,))
            cliente['ordini'] = cur.fetchall()
        conn.close()
        return jsonify(cliente), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── POST /api/clienti  ───────────────────────────────────────────────
@clienti_bp.route('/', methods=['POST'])
def crea_cliente():
    data = request.get_json()
    if not data or not data.get('nome') or not data.get('cognome'):
        return jsonify({'error': 'Campi "nome" e "cognome" obbligatori'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clienti (id_cliente, nome, cognome, email, ind_consegna)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data.get('id_cliente'),
                data['nome'],
                data['cognome'],
                data.get('email'),
                data.get('ind_consegna')
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cliente creato'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── PUT /api/clienti/<id>  ───────────────────────────────────────────
@clienti_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_cliente(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clienti
                SET nome=%s, cognome=%s, email=%s, ind_consegna=%s
                WHERE id_cliente=%s
            """, (
                data.get('nome'),
                data.get('cognome'),
                data.get('email'),
                data.get('ind_consegna'),
                id
            ))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Cliente non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cliente aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DELETE /api/clienti/<id>  ────────────────────────────────────────
@clienti_bp.route('/<int:id>', methods=['DELETE'])
def elimina_cliente(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clienti WHERE id_cliente = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Cliente non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cliente eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
