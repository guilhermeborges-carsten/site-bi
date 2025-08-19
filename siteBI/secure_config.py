# -*- coding: utf-8 -*-
"""
Módulo de configuração segura para o Site BI
Usa criptografia local AES para proteger configurações sensíveis
"""

import os
import sys
from local_crypto import LocalCryptoManager

class SecureConfig:
    """Classe para gerenciar configurações criptografadas"""
    
    def __init__(self):
        self.crypto = LocalCryptoManager()
        self._config = None
        self._load_config()
    
    def _load_config(self):
        """Carrega a configuração descriptografada"""
        try:
            # Verificar se existe arquivo criptografado
            if os.path.exists('config.encrypted'):
                print("🔐 Carregando configuração criptografada...")
                with open('config.encrypted', 'r', encoding='utf-8') as f:
                    encrypted_content = f.read()
                
                # Descriptografar
                config_content = self.crypto.decrypt_data(encrypted_content)
                
                # Executar o conteúdo descriptografado
                config_globals = {}
                exec(config_content, config_globals)
                
                # Extrair as classes de configuração
                self._config = {
                    'development': config_globals.get('DevelopmentConfig'),
                    'production': config_globals.get('ProductionConfig'),
                    'default': config_globals.get('DevelopmentConfig')
                }
                print("✅ Configuração criptografada carregada com sucesso!")
                
            else:
                # Fallback para configuração não criptografada
                print("📋 Arquivo criptografado não encontrado, usando fallback...")
                self._config = self._load_fallback_config()
                
        except Exception as e:
            print(f"⚠️  Erro ao carregar configuração criptografada: {str(e)}")
            print("📋 Usando configuração de fallback...")
            self._config = self._load_fallback_config()
    
    def _load_fallback_config(self):
        """Carrega configuração de fallback ou cria uma padrão"""
        try:
            # Verificar se estamos em desenvolvimento (arquivo config.py normal existe)
            if os.path.exists('config.py') and not self._is_config_encrypted():
                print("🔧 Carregando configuração de desenvolvimento...")
                return self._load_dev_config()
            else:
                # Em produção ou sem configuração, criar padrão
                print("🔧 Criando configuração padrão para produção...")
                return self._create_default_config()
                
        except Exception as e:
            print(f"⚠️  Erro ao carregar configuração: {str(e)}")
            return self._create_default_config()
    
    def _is_config_encrypted(self):
        """Verifica se o config.py atual está criptografado"""
        try:
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()
            return 'ENCRYPTED_CONFIG' in content
        except:
            return True
    
    def _load_dev_config(self):
        """Carrega configuração de desenvolvimento do config.py normal"""
        try:
            # Importar diretamente do config.py
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", "config.py")
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            
            return {
                'development': config_module.DevelopmentConfig,
                'production': config_module.ProductionConfig,
                'default': config_module.DevelopmentConfig
            }
        except Exception as e:
            print(f"⚠️  Erro ao carregar config.py: {str(e)}")
            return self._create_default_config()
    
    def _create_default_config(self):
        """Cria uma configuração padrão mínima"""
        print("🔧 Criando configuração padrão mínima...")
        
        class DefaultConfig:
            SECRET_KEY = 'sua_chave_secreta_aqui'
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            UPLOAD_FOLDER = 'uploads'
            MAX_CONTENT_LENGTH = 16 * 1024 * 1024
            MYSQL_HOST = 'localhost'
            MYSQL_PORT = 3306
            MYSQL_USER = 'root'
            MYSQL_PASSWORD = ''
            MYSQL_DATABASE = 'teste'
            
            @staticmethod
            def init_app(app):
                # Configurar URI do banco
                app.config['SQLALCHEMY_DATABASE_URI'] = (
                    f'mysql://{DefaultConfig.MYSQL_USER}:{DefaultConfig.MYSQL_PASSWORD}@'
                    f'{DefaultConfig.MYSQL_HOST}:{DefaultConfig.MYSQL_PORT}/{DefaultConfig.MYSQL_DATABASE}'
                )
        
        return {
            'development': DefaultConfig,
            'production': DefaultConfig,
            'default': DefaultConfig
        }
    
    def get_config(self, config_name='default'):
        """Retorna a configuração solicitada"""
        return self._config.get(config_name, self._config['default'])
    
    def get_database_uri(self, config_name='default'):
        """Retorna a URI do banco de dados descriptografada"""
        config_class = self.get_config(config_name)
        
        if hasattr(config_class, 'MYSQL_PASSWORD') and config_class.MYSQL_PASSWORD:
            return (
                f'mysql://{config_class.MYSQL_USER}:{config_class.MYSQL_PASSWORD}@'
                f'{config_class.MYSQL_HOST}:{config_class.MYSQL_PORT}/{config_class.MYSQL_DATABASE}'
            )
        else:
            return (
                f'mysql://{config_class.MYSQL_USER}@'
                f'{config_class.MYSQL_HOST}:{config_class.MYSQL_PORT}/{config_class.MYSQL_DATABASE}'
            )

# Instância global
secure_config = SecureConfig()

# Funções de conveniência
def get_config(config_name='default'):
    """Retorna a configuração solicitada"""
    return secure_config.get_config(config_name)

def get_database_uri(config_name='default'):
    """Retorna a URI do banco de dados"""
    return secure_config.get_database_uri(config_name)

# Configuração para compatibilidade com o sistema existente
config = {
    'development': get_config('development'),
    'production': get_config('production'),
    'default': get_config('default')
}
