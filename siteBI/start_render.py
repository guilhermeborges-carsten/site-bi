#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização para o Render
Configura ambiente e inicia aplicação com criptografia automática
"""

import os
import sys
import signal
import atexit

def setup_render_environment():
    """Configura ambiente para o Render"""
    print("🚀 Configurando ambiente para o Render...")
    
    # Definir variáveis de ambiente
    os.environ['RENDER'] = 'true'
    os.environ['PRODUCTION'] = 'true'
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = 'false'
    
    print("✅ Ambiente configurado para produção!")

def main():
    """Função principal"""
    print("🔐 Iniciando Site BI no Render...")
    
    # Configurar ambiente
    setup_render_environment()
    
    # Importar e executar aplicação
    try:
        from app import app
        
        # Configurar host e porta para o Render
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0'
        
        print(f"🌐 Iniciando servidor na porta {port}...")
        app.run(host=host, port=port)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
