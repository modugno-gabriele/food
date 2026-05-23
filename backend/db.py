import pymysql
import pymysql.cursors
from flask import current_app

def get_connection():
    """
    Apre e restituisce una connessione al database TiDB/MySQL.
    Usa DictCursor per ottenere le righe come dizionari Python.
    """
    cfg = current_app.config

    params = dict(
        host    = cfg['DB_HOST'],
        port    = cfg['DB_PORT'],
        user    = cfg['DB_USER'],
        password= cfg['DB_PASSWORD'],
        database= cfg['DB_NAME'],
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor,
        autocommit  = False,
    )

    # SSL opzionale (richiesto da TiDB Cloud)
    if cfg.get('DB_SSL_CA'):
        params['ssl'] = {'ca': cfg['DB_SSL_CA']}

    return pymysql.connect(**params)
