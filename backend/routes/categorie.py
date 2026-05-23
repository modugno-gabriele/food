from flask import Blueprint, jsonify, request
from db import get_connection

categorie_bp = Blueprint('categorie', __name__)

# ── GET /api/categorie  ──────────────────────────────────────────────
@categorie_bp.route('/', methods=['GET'])
def lista_categorie():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categoria_ristorante ORDER BY nome")
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET /api/categorie/<id>  ─────────────────────────────────────────
@categorie_bp.route('/<int:id>', methods=['GET'])
def dettaglio_categoria(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categoria_ristorante WHERE id_categoria = %s", (id,))
            row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'Categoria non trovata'}), 404
        return jsonify(row), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── POST /api/categorie  ─────────────────────────────────────────────
@categorie_bp.route('/', methods=['POST'])
def crea_categoria():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({'error': 'Campo "nome" obbligatorio'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO categoria_ristorante (id_categoria, nome, descrizione) VALUES (%s, %s, %s)",
                (data.get('id_categoria'), data['nome'], data.get('descrizione'))
            )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Categoria creata'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── PUT /api/categorie/<id>  ─────────────────────────────────────────
@categorie_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_categoria(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE categoria_ristorante SET nome=%s, descrizione=%s WHERE id_categoria=%s",
                (data.get('nome'), data.get('descrizione'), id)
            )
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Categoria non trovata'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Categoria aggiornata'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DELETE /api/categorie/<id>  ──────────────────────────────────────
@categorie_bp.route('/<int:id>', methods=['DELETE'])
def elimina_categoria(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM categoria_ristorante WHERE id_categoria = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Categoria non trovata'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Categoria eliminata'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
