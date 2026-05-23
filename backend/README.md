# 🍔 Food Delivery — Backend Flask

## Avvio rapido

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # modifica le credenziali TiDB
python app.py
```

Il server parte su `http://localhost:5000`.

---

## Configurazione TiDB

Apri `config.py` (o `.env`) e inserisci:

| Variabile | Valore |
|-----------|--------|
| `DB_HOST` | Host TiDB Cloud (es. `gateway01.eu-central-1...`) |
| `DB_PORT` | `4000` |
| `DB_USER` | Utente TiDB |
| `DB_PASSWORD` | Password TiDB |
| `DB_NAME` | `food` |

---

## 📋 Documentazione API

### Categorie — `/api/categorie`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/categorie/` | Lista tutte le categorie |
| GET | `/api/categorie/<id>` | Dettaglio categoria |
| POST | `/api/categorie/` | Crea categoria |
| PUT | `/api/categorie/<id>` | Modifica categoria |
| DELETE | `/api/categorie/<id>` | Elimina categoria |

### Ristoranti — `/api/ristoranti`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/ristoranti/` | Lista (filtri: `?cerca=`, `?categoria=`) |
| GET | `/api/ristoranti/<id>` | Dettaglio + piatti + media voto |
| POST | `/api/ristoranti/` | Crea ristorante |
| PUT | `/api/ristoranti/<id>` | Modifica ristorante |
| DELETE | `/api/ristoranti/<id>` | Elimina ristorante |

### Piatti — `/api/piatti`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/piatti/` | Lista (filtri: `?cerca=`, `?ristorante=`, `?disponibile=`) |
| GET | `/api/piatti/<id>` | Dettaglio + ingredienti |
| POST | `/api/piatti/` | Crea piatto |
| PUT | `/api/piatti/<id>` | Modifica piatto |
| DELETE | `/api/piatti/<id>` | Elimina piatto |

### Clienti — `/api/clienti`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/clienti/` | Lista (filtro: `?cerca=`) |
| GET | `/api/clienti/<id>` | Dettaglio + storico ordini |
| POST | `/api/clienti/` | Crea cliente |
| PUT | `/api/clienti/<id>` | Modifica cliente |
| DELETE | `/api/clienti/<id>` | Elimina cliente |

### Ordini — `/api/ordini`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/ordini/` | Lista (filtri: `?stato=`, `?cliente=`) |
| GET | `/api/ordini/<id>` | Dettaglio completo con piatti |
| POST | `/api/ordini/` | Crea ordine (accetta array `piatti`) |
| PUT | `/api/ordini/<id>` | Aggiorna stato/fattorino |
| DELETE | `/api/ordini/<id>` | Elimina ordine |

### Fattorini — `/api/fattorini`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/fattorini/` | Lista (filtro: `?disponibile=1`) |
| GET | `/api/fattorini/<id>` | Dettaglio fattorino |
| POST | `/api/fattorini/` | Crea fattorino |
| PUT | `/api/fattorini/<id>` | Modifica fattorino |
| DELETE | `/api/fattorini/<id>` | Elimina fattorino |

### Recensioni — `/api/recensioni`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/recensioni/` | Lista (filtri: `?ristorante=`, `?cliente=`) |
| GET | `/api/recensioni/<id>` | Dettaglio recensione |
| POST | `/api/recensioni/` | Crea recensione |
| PUT | `/api/recensioni/<id>` | Modifica recensione |
| DELETE | `/api/recensioni/<id>` | Elimina recensione |

### Ingredienti — `/api/ingredienti`

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/ingredienti/` | Lista (filtri: `?cerca=`, `?allergenico=1`) |
| GET | `/api/ingredienti/<id>` | Dettaglio ingrediente |
| POST | `/api/ingredienti/` | Crea ingrediente |
| PUT | `/api/ingredienti/<id>` | Modifica ingrediente |
| DELETE | `/api/ingredienti/<id>` | Elimina ingrediente |

---

## Struttura del progetto

```
backend/
├── app.py              ← entry point Flask, registra i Blueprint
├── config.py           ← configurazione DB e app
├── db.py               ← helper connessione TiDB/MySQL
├── requirements.txt
├── .env.example
└── routes/
    ├── __init__.py
    ├── categorie.py
    ├── ristoranti.py
    ├── piatti.py
    ├── clienti.py
    ├── ordini.py
    ├── fattorini.py
    ├── recensioni.py
    └── ingredienti.py
```

## Codici HTTP usati

| Codice | Significato |
|--------|-------------|
| 200 | OK |
| 201 | Creato |
| 400 | Dati mancanti o non validi |
| 404 | Risorsa non trovata |
| 500 | Errore interno del server |
