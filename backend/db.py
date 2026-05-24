import pymysql
import pymysql.cursors
from flask import current_app

def get_connection():
    cfg = current_app.config
    params = dict(
        host        = cfg['DB_HOST'],
        port        = cfg['DB_PORT'],
        user        = cfg['DB_USER'],
        password    = cfg['DB_PASSWORD'],
        database    = cfg['DB_NAME'],
        charset     = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor,
        autocommit  = False,
        ssl         = {'ca': '/etc/ssl/certs/ca-certificates.crt'}
    )
    return pymysql.connect(**params)
