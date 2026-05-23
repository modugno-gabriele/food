from flask import Blueprint, jsonify, request
from db import get_connection

ingredienti_bp = Blueprint('ingredienti', __name__)

@ingredienti_bp.route('/', methods=['GET'])
def lista_ingredienti():
    allergenico = request.args.get('allergenico')
    cerca       = request.args.get('cerca', '')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            sql = "SELECT * FROM ingrediente WHERE nome LIKE %s"
            params = [f'%{cerca}%']
            if allergenico is not None:
                sql += " AND allergenico = %s"
                params.append(allergenico == '1' or allergenico == 'true')
            sql += " ORDER BY nome"
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredienti_bp.route('/<int:id>', methods=['GET'])
def dettaglio_ingrediente(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ingrediente WHERE id_ingrediente = %s", (id,))
            row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'Ingrediente non trovato'}), 404
        return jsonify(row), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredienti_bp.route('/', methods=['POST'])
def crea_ingrediente():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({'error': 'Campo "nome" obbligatorio'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ingrediente (id_ingrediente, nome, allergenico)
                VALUES (%s, %s, %s)
            """, (data.get('id_ingrediente'), data['nome'], data.get('allergenico', False)))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ingrediente creato'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredienti_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_ingrediente(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE ingrediente SET nome=%s, allergenico=%s WHERE id_ingrediente=%s
            """, (data.get('nome'), data.get('allergenico'), id))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Ingrediente non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ingrediente aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredienti_bp.route('/<int:id>', methods=['DELETE'])
def elimina_ingrediente(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM ingrediente WHERE id_ingrediente = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Ingrediente non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ingrediente eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
