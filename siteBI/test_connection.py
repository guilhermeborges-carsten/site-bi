#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar conexão MySQL sem especificar banco
"""

import pymysql
from config import config

def test_mysql_connection():
    """Testa conexão MySQL básica"""
    
    config_obj = config['development']
    
    try:
        # Conectar sem especificar banco
        connection = pymysql.connect(
            host=config_obj.MYSQL_HOST,
            port=config_obj.MYSQL_PORT,
            user=config_obj.MYSQL_USER,
            password=config_obj.MYSQL_PASSWORD,
            charset='utf8'
        )
        
        print("✅ Conexão MySQL estabelecida com sucesso!")
        
        with connection.cursor() as cursor:
            # Listar bancos disponíveis
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            print(f"\n📋 Bancos disponíveis no servidor:")
            for db in databases:
                print(f"  - {db[0]}")
            
            # Verificar se PAINEL_BI existe
            bi_exists = any(db[0] == 'PAINEL_BI' for db in databases)
            
            if bi_exists:
                print("\n✅ Banco 'PAINEL_BI' encontrado!")
                
                # Conectar ao banco PAINEL_BI
                connection.select_db('PAINEL_BI')
                
                # Listar tabelas
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                print(f"\n📊 Tabelas no banco 'BI':")
                for table in tables:
                    print(f"  - {table[0]}")
                    
            else:
                print("\n❌ Banco 'PAINEL_BI' NÃO encontrado!")
                print("💡 Você precisa criar o banco 'PAINEL_BI' primeiro.")
                print("💡 Execute: CREATE DATABASE IF NOT EXISTS `PAINEL_BI`;")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 Testando conexão MySQL...")
    print("=" * 50)
    
    test_mysql_connection()
