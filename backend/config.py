import os


class Config:
    DB_USER = os.getenv('DB_USER', os.getenv('DB_USER', 'postgres'))
    DB_PASSWORD = os.getenv('DB_PASSWORD', os.getenv('DB_PASSWORD', 'postgres'))
    DB_HOST = os.getenv('DB_HOST', os.getenv('DB_HOST', 'localhost'))
    DB_PORT = os.getenv('RDS_PORT', os.getenv('DB_PORT', '5432'))
    DB_PORT = int(DB_PORT) if DB_PORT.isdigit() else 5432
    DB_NAME = os.getenv('RDS_DB_NAME', os.getenv('DB_NAME', 'evaluaciones_db'))
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    def __init__(self):
        print(f'SQLALCHEMY_DATABASE_URI: {self.SQLALCHEMY_DATABASE_URI}')
