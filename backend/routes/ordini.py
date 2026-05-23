from flask import Blueprint, jsonify, request
from db import get_connection

ordini_bp = Blueprint('ordini', __name__)

# ── GET /api/ordini  (lista + filtri stato/cliente) ───────────────────
@ordini_bp.route('/', methods=['GET'])
def lista_ordini():
    stato      = request.args.get('stato')
    id_cliente = request.args.get('cliente')
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            sql = """
                SELECT o.*,
                       CONCAT(c.nome, ' ', c.cognome) AS cliente,
                       f.nome AS fattorino
                FROM ordine o
                JOIN clienti  c ON o.id_cliente  = c.id_cliente
                LEFT JOIN fattorino f ON o.id_fattorino = f.id_fattorino
                WHERE 1=1
            """
            params = []
            if stato:
                sql += " AND o.stato = %s"
                params.append(stato)
            if id_cliente:
                sql += " AND o.id_cliente = %s"
                params.append(id_cliente)
            sql += " ORDER BY o.data_ora DESC"
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET /api/ordini/<id>  (dettaglio completo con piatti) ────────────
@ordini_bp.route('/<int:id>', methods=['GET'])
def dettaglio_ordine(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT o.*,
                       CONCAT(c.nome, ' ', c.cognome) AS cliente,
                       c.ind_consegna,
                       f.nome AS fattorino,
                       f.mezzo
                FROM ordine o
                JOIN clienti  c ON o.id_cliente  = c.id_cliente
                LEFT JOIN fattorino f ON o.id_fattorino = f.id_fattorino
                WHERE o.id_ordine = %s
            """, (id,))
            ordine = cur.fetchone()
            if not ordine:
                conn.close()
                return jsonify({'error': 'Ordine non trovato'}), 404

            cur.execute("""
                SELECT p.nome AS piatto, p.prezzo, do.quantita, do.prez_unit,
                       (do.quantita * do.prez_unit) AS subtotale
                FROM dettaglio_ordine do
                JOIN piatto p ON do.id_piatto = p.id_piatto
                WHERE do.id_ordine = %s
            """, (id,))
            ordine['dettaglio'] = cur.fetchall()
        conn.close()
        return jsonify(ordine), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── POST /api/ordini  ────────────────────────────────────────────────
@ordini_bp.route('/', methods=['POST'])
def crea_ordine():
    data = request.get_json()
    if not data or not data.get('id_cliente'):
        return jsonify({'error': 'Campo "id_cliente" obbligatorio'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ordine (id_ordine, id_cliente, id_fattorino, data_ora, stato, totale)
                VALUES (%s, %s, %s, NOW(), %s, %s)
            """, (
                data.get('id_ordine'),
                data['id_cliente'],
                data.get('id_fattorino'),
                data.get('stato', 'Creato'),
                data.get('totale', 0)
            ))
            # Inserimento righe dettaglio se presenti
            piatti = data.get('piatti', [])
            for p in piatti:
                cur.execute("""
                    INSERT INTO dettaglio_ordine (id_ordine, id_piatto, quantita, prez_unit)
                    VALUES (%s, %s, %s, %s)
                """, (
                    data.get('id_ordine'),
                    p['id_piatto'],
                    p.get('quantita', 1),
                    p.get('prez_unit', 0)
                ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ordine creato'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── PUT /api/ordini/<id>  (modifica stato o fattorino) ───────────────
@ordini_bp.route('/<int:id>', methods=['PUT'])
def aggiorna_ordine(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati mancanti'}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE ordine
                SET stato=%s, id_fattorino=%s, totale=%s
                WHERE id_ordine=%s
            """, (
                data.get('stato'),
                data.get('id_fattorino'),
                data.get('totale'),
                id
            ))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Ordine non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ordine aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DELETE /api/ordini/<id>  ─────────────────────────────────────────
@ordini_bp.route('/<int:id>', methods=['DELETE'])
def elimina_ordine(id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Prima elimina i dettagli (FK constraint)
            cur.execute("DELETE FROM dettaglio_ordine WHERE id_ordine = %s", (id,))
            cur.execute("DELETE FROM ordine WHERE id_ordine = %s", (id,))
            if cur.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Ordine non trovato'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ordine eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
