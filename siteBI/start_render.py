#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização para o Render
Configura ambiente e inicia aplicação com criptografia automática
"""

import os
import sys
import traceback
import logging

# Configurar logging para debug
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_render_environment():
    """Configura ambiente para o Render"""
    try:
        logger.info("🚀 Configurando ambiente para o Render...")
        
        # Definir variáveis de ambiente
        os.environ['RENDER'] = 'true'
        os.environ['PRODUCTION'] = 'true'
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = 'false'
        
        logger.info("✅ Ambiente configurado para produção!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar ambiente: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def decrypt_config_for_render():
    """Descriptografa configuração para o Render sem precisar de backup"""
    try:
        logger.info("🔓 Descriptografando configuração para o Render...")
        
        if not os.path.exists('config.py.encrypted'):
            logger.error("❌ Arquivo config.py.encrypted não encontrado!")
            return False
        
        # Importar sistema de criptografia
        from local_crypto import LocalCryptoManager
        crypto = LocalCryptoManager()
        
        # Ler arquivo criptografado
        with open('config.py.encrypted', 'r', encoding='utf-8') as f:
            encrypted_content = f.read()
        
        # Descriptografar
        decrypted_content = crypto.decrypt_data(encrypted_content)
        
        # Salvar configuração descriptografada
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(decrypted_content)
        
        logger.info("✅ Configuração descriptografada para o Render!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao descriptografar: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    try:
        logger.info("📦 Verificando dependências...")
        
        # Verificar dependências críticas
        import flask
        import flask_sqlalchemy
        import flask_login
        from cryptography.fernet import Fernet
        
        logger.info("✅ Todas as dependências estão instaladas!")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Dependência não encontrada: {str(e)}")
        logger.error("Execute: pip install -r requirements.txt")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao verificar dependências: {str(e)}")
        return False

def check_files():
    """Verifica se arquivos essenciais existem"""
    try:
        logger.info("📁 Verificando arquivos essenciais...")
        
        required_files = [
            'app.py',
            'local_crypto.py',
            'secure_config.py',
            'config.py.encrypted'
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                logger.error(f"❌ Arquivo não encontrado: {file}")
                return False
        
        logger.info("✅ Todos os arquivos essenciais existem!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar arquivos: {str(e)}")
        return False

def main():
    """Função principal"""
    try:
        logger.info("🔐 Iniciando Site BI no Render...")
        
        # Verificar dependências
        if not check_dependencies():
            logger.error("❌ Falha na verificação de dependências")
            sys.exit(1)
        
        # Verificar arquivos
        if not check_files():
            logger.error("❌ Falha na verificação de arquivos")
            sys.exit(1)
        
        # Configurar ambiente
        if not setup_render_environment():
            logger.error("❌ Falha na configuração do ambiente")
            sys.exit(1)
        
        # Descriptografar configuração para o Render
        if not decrypt_config_for_render():
            logger.error("❌ Falha ao descriptografar configuração")
            sys.exit(1)
        
        # Importar e executar aplicação
        try:
            logger.info("📱 Importando aplicação...")
            from app import app
            
            # Configurar host e porta para o Render
            port = int(os.environ.get('PORT', 5000))
            host = '0.0.0.0'
            
            logger.info(f"🌐 Iniciando servidor na porta {port}...")
            logger.info("✅ Aplicação iniciada com sucesso!")
            
            app.run(host=host, port=port, debug=False)
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar aplicação: {str(e)}")
            logger.error(traceback.format_exc())
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Erro crítico: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
