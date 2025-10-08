import os
from datetime import timedelta

class Config:
    # Configurações de Segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SESSION_COOKIE_SECURE = False  # Mudar para True em produção com HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Configurações do Flask
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_timeout': 20,
        'max_overflow': 10,
        'pool_size': 5
    }
    
    # Configurações de Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    FORBIDDEN_EXTENSIONS = {'php', 'asp', 'jsp', 'exe', 'sh', 'bat', 'vbs', 'js', 'py', 'pl', 'rb'}
    
    # Configurações de Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "200 per day;50 per hour;10 per minute"
    
    # Configurações de Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurações de Criptografia
    BCRYPT_LOG_ROUNDS = 12
    
    # Configurações de Sessão
    SESSION_TYPE = 'filesystem'
    
    @staticmethod
    def init_app(app):
        # Configurar a URI do banco de dados MySQL com validação
        mysql_host = os.environ.get('MYSQL_HOST', '46.202.151.75')
        mysql_port = int(os.environ.get('MYSQL_PORT', 3306))
        mysql_user = os.environ.get('MYSQL_USER', 'user_bi')
        mysql_password = os.environ.get('MYSQL_PASSWORD', 'sk15iY4rVGLCoqK0')
        mysql_database = os.environ.get('MYSQL_DATABASE', 'BI')
        
        # Validação das configurações
        if not mysql_host or not mysql_user or not mysql_database:
            raise ValueError("Configurações do banco de dados incompletas")
        
        # Construir URI do banco com escape adequado
        if mysql_password:
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                f'mysql://{mysql_user}:{mysql_password}@'
                f'{mysql_host}:{mysql_port}/{mysql_database}'
                '?charset=utf8mb4&ssl_mode=REQUIRED'
            )
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                f'mysql://{mysql_user}@'
                f'{mysql_host}:{mysql_port}/{mysql_database}'
                '?charset=utf8mb4'
            )
        
        # Configurações adicionais de segurança
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['WTF_CSRF_TIME_LIMIT'] = 3600
        
        # Configurações de headers de segurança
        app.config['SECURITY_HEADERS'] = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        }

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Permitir HTTP em desenvolvimento
    
    # Configurações específicas para desenvolvimento
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_timeout': 20,
        'max_overflow': 5,
        'pool_size': 3,
        'echo': True  # Log de queries SQL
    }

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    
    # Usar banco de teste
    MYSQL_DATABASE = os.environ.get('MYSQL_TEST_DATABASE', 'BI_TEST')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Configurações de produção mais restritivas
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Logs mais detalhados em produção
    LOG_LEVEL = 'WARNING'
    
    # Configurações de banco mais robustas para produção
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_timeout': 30,
        'max_overflow': 20,
        'pool_size': 10,
        'echo': False
    }

# Configuração baseada no ambiente
def get_config():
    env = os.environ.get('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig

# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': get_config()
}

# Função para validar configurações
def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    required_vars = [
        'MYSQL_HOST',
        'MYSQL_USER', 
        'MYSQL_DATABASE'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Variáveis de ambiente obrigatórias não definidas: {', '.join(missing_vars)}")
    
    return True
