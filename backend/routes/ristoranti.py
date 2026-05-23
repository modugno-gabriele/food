from flask import Blueprint, jsonify, request
from db import get_connection

ristoranti_bp = Blueprint('ristoranti', __name__)

# ── GET /api/ristoranti  (lista + filtro per categoria + ricerca nome) ──
@ristoranti_bp.route('/', methods=['GET'])
def lista_ristoranti():
    id_categoria = request.args.get('categoria')
    cerca        = request.args.get('cerca', '')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            sql = """
                SELECT r.*, c.nome AS categoria
                FROM ristorante r
                JOIN categoria_ristorante c ON r.id_categoria = c.id_categoria
                WHERE r.nome LIKE %s
            """
            params = [f'%{cerca}%']
            if id_categoria:
                sql += " AND r.id_categoria = %s"
                params.append(id_categoria)
            sql += " ORDER BY r.nome"
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET /api/ristoranti/<id>  (dettaglio + piatti + media voto) ──────
@ristoranti_bp.route('/<int:id>', methods=['GET'])
def dettaglio_ristorante(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Ristorante base
            cur.execute("""
                SELECT r.*, c.nome AS categoria
                FROM ristorante r
                JOIN categoria_ristorante c ON r.id_categoria = c.id_categoria
                WHERE r.id_ristorante = %s
            """, (id,))
            ristorante = cur.fetchone()
            if not ristorante:
                conn.close()
                return jsonify({'error': 'Ristorante non trovato'}), 404

            # Piatti del ristorante
            cur.execute("""
                SELECT * FROM piatto WHERE id_ristorante = %s ORDER BY nome
            """, (id,))
            ristorante['piatti'] = cur.fetchall()

            # Media voto recensioni
            cur.execute("""
                SELECT ROUND(AVG(voto), 1) AS media_voto, COUNT(*) AS num_recensioni
                FROM recensioni WHERE id_ristorante = %s
            """, (id,))
            stats = cur.fetchone()
            ristorante['media_voto']     = stats['media_voto']
            ristorante['num_recensioni'] = stats['num_recensioni']

        conn.close()
        return jsonify(ristorante), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── POST /api/ristoranti  ────────────────────────────────────────────
@ristoranti_bp.route('/', methods=['POST'])
def crea_ristorante():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({'error': 'Campo "nome" obbligatorio'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ristorante (id_ristorante, id_categoria, nome, indirizzo, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data.get('id_ristorante'),
                data.get('id_categoria'),
                data['nome'],
                data.get('indirizzo'),
                data.get('telefono')
            ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ristorante creato'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── PUT /api/ristoranti/<id>  ────────────────────────────────────────
@ristoranti_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_ristorante(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE ristorante
                SET id_categoria=%s, nome=%s, indirizzo=%s, telefono=%s
                WHERE id_ristorante=%s
            """, (
                data.get('id_categoria'),
                data.get('nome'),
                data.get('indirizzo'),
                data.get('telefono'),
                id
            ))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Ristorante non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ristorante aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DELETE /api/ristoranti/<id>  ─────────────────────────────────────
@ristoranti_bp.route('/<int:id>', methods=['DELETE'])
def elimina_ristorante(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM ristorante WHERE id_ristorante = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Ristorante non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ristorante eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
