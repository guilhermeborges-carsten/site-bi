import os

class Config:
    SECRET_KEY = 'sua_chave_secreta_aqui'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configuração do banco MySQL
    # Altere estas configurações conforme seu ambiente
    MYSQL_HOST = '46.202.151.75'
    MYSQL_PORT = 3306
    MYSQL_USER = 'user_bi'
    MYSQL_PASSWORD = 'sk15iY4rVGLCoqK0'  # Deixe vazio se não tiver senha
    MYSQL_DATABASE = 'BI'
    
    @staticmethod
    def init_app(app):
        # Configurar a URI do banco de dados MySQL
        if Config.MYSQL_PASSWORD:
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                f'mysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@'
                f'{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}'
            )
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                f'mysql://{Config.MYSQL_USER}@'
                f'{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}'
            )

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
