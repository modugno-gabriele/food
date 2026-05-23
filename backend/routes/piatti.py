from flask import Blueprint, jsonify, request
from db import get_connection

piatti_bp = Blueprint('piatti', __name__)

# ── GET /api/piatti  (lista + filtro ristorante + ricerca nome) ───────
@piatti_bp.route('/', methods=['GET'])
def lista_piatti():
    id_ristorante = request.args.get('ristorante')
    cerca         = request.args.get('cerca', '')
    disponibile   = request.args.get('disponibile')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            sql = """
                SELECT p.*, r.nome AS ristorante
                FROM piatto p
                JOIN ristorante r ON p.id_ristorante = r.id_ristorante
                WHERE p.nome LIKE %s
            """
            params = [f'%{cerca}%']
            if id_ristorante:
                sql += " AND p.id_ristorante = %s"
                params.append(id_ristorante)
            if disponibile is not None:
                sql += " AND p.disponibile = %s"
                params.append(disponibile == '1' or disponibile == 'true')
            sql += " ORDER BY p.nome"
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET /api/piatti/<id>  (dettaglio + ingredienti) ──────────────────
@piatti_bp.route('/<int:id>', methods=['GET'])
def dettaglio_piatto(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.*, r.nome AS ristorante
                FROM piatto p
                JOIN ristorante r ON p.id_ristorante = r.id_ristorante
                WHERE p.id_piatto = %s
            """, (id,))
            piatto = cur.fetchone()
            if not piatto:
                conn.close()
                return jsonify({'error': 'Piatto non trovato'}), 404

            cur.execute("""
                SELECT i.id_ingrediente, i.nome, i.allergenico
                FROM ingrediente i
                JOIN composizione_piatto cp ON i.id_ingrediente = cp.id_ingrediente
                WHERE cp.id_piatto = %s
            """, (id,))
            piatto['ingredienti'] = cur.fetchall()
        conn.close()
        return jsonify(piatto), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── POST /api/piatti  ────────────────────────────────────────────────
@piatti_bp.route('/', methods=['POST'])
def crea_piatto():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({'error': 'Campo "nome" obbligatorio'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO piatto (id_piatto, id_ristorante, nome, prezzo, disponibile)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data.get('id_piatto'),
                data.get('id_ristorante'),
                data['nome'],
                data.get('prezzo', 0),
                data.get('disponibile', True)
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Piatto creato'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── PUT /api/piatti/<id>  ────────────────────────────────────────────
@piatti_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_piatto(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE piatto
                SET id_ristorante=%s, nome=%s, prezzo=%s, disponibile=%s
                WHERE id_piatto=%s
            """, (
                data.get('id_ristorante'),
                data.get('nome'),
                data.get('prezzo'),
                data.get('disponibile'),
                id
            ))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Piatto non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Piatto aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DELETE /api/piatti/<id>  ─────────────────────────────────────────
@piatti_bp.route('/<int:id>', methods=['DELETE'])
def elimina_piatto(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM piatto WHERE id_piatto = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Piatto non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Piatto eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
