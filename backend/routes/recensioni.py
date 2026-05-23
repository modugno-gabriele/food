from flask import Blueprint, jsonify, request
from db import get_connection

recensioni_bp = Blueprint('recensioni', __name__)

@recensioni_bp.route('/', methods=['GET'])
def lista_recensioni():
    id_ristorante = request.args.get('ristorante')
    id_cliente    = request.args.get('cliente')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            sql = """
                SELECT rec.*,
                       CONCAT(c.nome, ' ', c.cognome) AS cliente,
                       r.nome AS ristorante
                FROM recensioni rec
                JOIN clienti c ON rec.id_cliente = c.id_cliente
                JOIN ristorante r ON rec.id_ristorante = r.id_ristorante
                WHERE 1=1
            """
            params = []
            if id_ristorante:
                sql += " AND rec.id_ristorante = %s"
                params.append(id_ristorante)
            if id_cliente:
                sql += " AND rec.id_cliente = %s"
                params.append(id_cliente)
            sql += " ORDER BY rec.data DESC"
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recensioni_bp.route('/<int:id>', methods=['GET'])
def dettaglio_recensione(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT rec.*,
                       CONCAT(c.nome, ' ', c.cognome) AS cliente,
                       r.nome AS ristorante
                FROM recensioni rec
                JOIN clienti c ON rec.id_cliente = c.id_cliente
                JOIN ristorante r ON rec.id_ristorante = r.id_ristorante
                WHERE rec.id_recensione = %s
            """, (id,))
            row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'Recensione non trovata'}), 404
        return jsonify(row), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recensioni_bp.route('/', methods=['POST'])
def crea_recensione():
    data = request.get_json()
    if not data or not data.get('id_cliente') or not data.get('id_ristorante') or data.get('voto') is None:
        return jsonify({'error': 'Campi "id_cliente", "id_ristorante" e "voto" obbligatori'}), 400
    voto = int(data['voto'])
    if not 1 <= voto <= 5:
        return jsonify({'error': 'Il voto deve essere compreso tra 1 e 5'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO recensioni (id_cliente, id_ristorante, data, commento, voto)
                VALUES (%s, %s, NOW(), %s, %s)
            """, (
                data['id_cliente'],
                data['id_ristorante'],
                data.get('commento'),
                voto
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Recensione creata'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recensioni_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_recensione(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE recensioni SET commento=%s, voto=%s WHERE id_recensione=%s
            """, (data.get('commento'), data.get('voto'), id))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Recensione non trovata'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Recensione aggiornata'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recensioni_bp.route('/<int:id>', methods=['DELETE'])
def elimina_recensione(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM recensioni WHERE id_recensione = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Recensione non trovata'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Recensione eliminata'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
