#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a conexão com o banco MySQL
"""

from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    
    # Criar app Flask temporário
    app = Flask(__name__)
    config_name = 'development'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Criar instância do SQLAlchemy
    db = SQLAlchemy(app)
    
    try:
        with app.app_context():
            # Testar conexão
            with db.engine.connect() as connection:
                result = connection.execute(db.text('SELECT 1 as test'))
                row = result.fetchone()
                
                if row and row[0] == 1:
                    print("✅ Conexão com banco MySQL estabelecida com sucesso!")
                    
                    # Testar algumas queries básicas
                    print("\n🔍 Testando queries básicas...")
                    
                    # Verificar se as tabelas existem
                    tables = connection.execute(db.text("SHOW TABLES"))
                    table_list = [table[0] for table in tables]
                    print(f"📋 Tabelas encontradas: {', '.join(table_list)}")
                    
                    # Verificar usuários
                    users = connection.execute(db.text("SELECT COUNT(*) as count FROM usuario"))
                    user_count = users.fetchone()[0]
                    print(f"👥 Usuários no banco: {user_count}")
                    
                    # Verificar chamados
                    chamados = connection.execute(db.text("SELECT COUNT(*) as count FROM chamado"))
                    chamado_count = chamados.fetchone()[0]
                    print(f"📝 Chamados no banco: {chamado_count}")
                    
                    print("\n🎉 Todos os testes passaram! O banco está funcionando perfeitamente.")
                    return True
                    
                else:
                    print("❌ Falha na conexão com o banco")
                    return False
                
    except Exception as e:
        print(f"❌ Erro ao conectar com o banco de dados: {str(e)}")
        print("\n🔧 Possíveis soluções:")
        print("1. Verifique se o MySQL está rodando")
        print("2. Verifique as configurações no config.py")
        print("3. Verifique se o usuário tem permissões no banco")
        print("4. Verifique se o banco 'BI' existe")
        return False

if __name__ == '__main__':
    print("🚀 Testando conexão com banco MySQL...")
    print("=" * 50)
    
    success = test_database_connection()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
