from flask import Flask
from flask_cors import CORS
from config import Config
from routes.ristoranti import ristoranti_bp
from routes.piatti import piatti_bp
from routes.clienti import clienti_bp
from routes.ordini import ordini_bp
from routes.fattorini import fattorini_bp
from routes.recensioni import recensioni_bp
from routes.ingredienti import ingredienti_bp
from routes.categorie import categorie_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Registrazione Blueprint
app.register_blueprint(ristoranti_bp, url_prefix='/api/ristoranti')
app.register_blueprint(piatti_bp, url_prefix='/api/piatti')
app.register_blueprint(clienti_bp, url_prefix='/api/clienti')
app.register_blueprint(ordini_bp, url_prefix='/api/ordini')
app.register_blueprint(fattorini_bp, url_prefix='/api/fattorini')
app.register_blueprint(recensioni_bp, url_prefix='/api/recensioni')
app.register_blueprint(ingredienti_bp, url_prefix='/api/ingredienti')
app.register_blueprint(categorie_bp, url_prefix='/api/categorie')

@app.route('/')
def index():
    return {'message': 'Food Delivery API funzionante ✅', 'version': '1.0'}, 200

@app.errorhandler(404)
def not_found(e):
    return {'error': 'Risorsa non trovata'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'error': 'Errore interno del server'}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
