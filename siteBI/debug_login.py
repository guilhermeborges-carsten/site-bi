#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para diagnosticar problemas de login no Sistema BI
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

def verificar_banco():
    """Verifica se o banco de dados existe e mostra informações"""
    db_path = 'instance/chamados.db'
    
    if not os.path.exists(db_path):
        print("❌ ERRO: Banco de dados não encontrado!")
        print(f"   Caminho esperado: {db_path}")
        return False
    
    print("✅ Banco de dados encontrado!")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        
        print(f"\n📋 Tabelas encontradas: {len(tabelas)}")
        for tabela in tabelas:
            print(f"   - {tabela[0]}")
        
        # Verificar usuários
        cursor.execute("SELECT id, nome, email, tipo FROM usuario;")
        usuarios = cursor.fetchall()
        
        print(f"\n👥 Usuários cadastrados: {len(usuarios)}")
        if usuarios:
            for user in usuarios:
                print(f"   ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Tipo: {user[3]}")
        else:
            print("   ⚠️  Nenhum usuário encontrado!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao acessar banco: {e}")
        return False

def criar_usuario_admin():
    """Cria um usuário administrador padrão"""
    db_path = 'instance/chamados.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se já existe um admin
        cursor.execute("SELECT id FROM usuario WHERE tipo='admin';")
        admin_existente = cursor.fetchone()
        
        if admin_existente:
            print("✅ Usuário admin já existe!")
            return True
        
        # Criar usuário admin padrão
        nome = "Administrador"
        email = "admin@sistema.com"
        senha = "admin123"
        senha_hash = generate_password_hash(senha)
        tipo = "admin"
        
        cursor.execute("""
            INSERT INTO usuario (nome, email, senha, tipo) 
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha_hash, tipo))
        
        conn.commit()
        conn.close()
        
        print("✅ Usuário admin criado com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print("   ⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao criar usuário: {e}")
        return False

def testar_login(email, senha):
    """Testa o login com as credenciais fornecidas"""
    db_path = 'instance/chamados.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buscar usuário
        cursor.execute("SELECT id, nome, email, senha, tipo FROM usuario WHERE email=?;", (email,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuário não encontrado: {email}")
            return False
        
        user_id, nome, user_email, senha_hash, tipo = usuario
        
        # Verificar senha
        if check_password_hash(senha_hash, senha):
            print(f"✅ Login válido!")
            print(f"   ID: {user_id}")
            print(f"   Nome: {nome}")
            print(f"   Email: {user_email}")
            print(f"   Tipo: {tipo}")
            return True
        else:
            print(f"❌ Senha incorreta para: {email}")
            return False
        
    except Exception as e:
        print(f"❌ ERRO ao testar login: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def mostrar_hash_senha(email):
    """Mostra o hash da senha de um usuário (para debug)"""
    db_path = 'instance/chamados.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT senha FROM usuario WHERE email=?;", (email,))
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"🔍 Hash da senha para {email}:")
            print(f"   {resultado[0]}")
            return True
        else:
            print(f"❌ Usuário não encontrado: {email}")
            return False
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Função principal do script"""
    print("🔍 DIAGNÓSTICO DO SISTEMA BI - LOGIN")
    print("=" * 50)
    
    # Verificar banco de dados
    if not verificar_banco():
        return
    
    # Criar usuário admin se necessário
    print("\n" + "=" * 50)
    print("🔧 CONFIGURAÇÃO INICIAL")
    criar_usuario_admin()
    
    # Testar login com usuário padrão
    print("\n" + "=" * 50)
    print("🧪 TESTE DE LOGIN")
    testar_login("admin@sistema.com", "admin123")
    
    print("\n" + "=" * 50)
    print("📝 INSTRUÇÕES:")
    print("1. Use as credenciais padrão:")
    print("   Email: admin@sistema.com")
    print("   Senha: admin123")
    print("2. Se não funcionar, verifique:")
    print("   - Se o Flask está rodando")
    print("   - Se não há erros no console")
    print("   - Se o banco de dados foi criado corretamente")
    print("3. Para criar um novo usuário, use a página de cadastro")

if __name__ == "__main__":
    main() 