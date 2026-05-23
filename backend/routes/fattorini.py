from flask import Blueprint, jsonify, request
from db import get_connection

fattorini_bp = Blueprint('fattorini', __name__)

@fattorini_bp.route('/', methods=['GET'])
def lista_fattorini():
    disponibile = request.args.get('disponibile')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            sql = "SELECT * FROM fattorino WHERE 1=1"
            params = []
            if disponibile is not None:
                sql += " AND disponibile = %s"
                params.append(disponibile == '1' or disponibile == 'true')
            sql += " ORDER BY nome"
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fattorini_bp.route('/<int:id>', methods=['GET'])
def dettaglio_fattorino(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM fattorino WHERE id_fattorino = %s", (id,))
            row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'Fattorino non trovato'}), 404
        return jsonify(row), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fattorini_bp.route('/', methods=['POST'])
def crea_fattorino():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({'error': 'Campo "nome" obbligatorio'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO fattorino (id_fattorino, nome, mezzo, disponibile)
                VALUES (%s, %s, %s, %s)
            """, (
                data.get('id_fattorino'),
                data['nome'],
                data.get('mezzo'),
                data.get('disponibile', True)
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Fattorino creato'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fattorini_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_fattorino(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE fattorino SET nome=%s, mezzo=%s, disponibile=%s
                WHERE id_fattorino=%s
            """, (data.get('nome'), data.get('mezzo'), data.get('disponibile'), id))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Fattorino non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Fattorino aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fattorini_bp.route('/<int:id>', methods=['DELETE'])
def elimina_fattorino(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fattorino WHERE id_fattorino = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Fattorino non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Fattorino eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
