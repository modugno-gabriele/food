import os

class Config:
    DB_HOST     = os.getenv('DB_HOST',     'gateway01.eu-central-1.prod.aws.tidbcloud.com')
    DB_PORT     = int(os.getenv('DB_PORT', 4000))
    DB_USER     = os.getenv('DB_USER',     '2SZc5k7KdZYPqyW.root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '9pD7h08mGxU1RWi0')
    DB_NAME     = os.getenv('DB_NAME',     'Food')
    DB_SSL_CA   = os.getenv('DB_SSL_CA',   '') 

    DEBUG = True
    JSON_SORT_KEYS = False
