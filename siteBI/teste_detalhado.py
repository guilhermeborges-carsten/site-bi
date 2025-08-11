#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste detalhado do sistema de login
"""

import sqlite3
import os
from werkzeug.security import check_password_hash

def testar_banco_detalhado():
    """Teste detalhado do banco de dados"""
    print("🔍 TESTE DETALHADO DO BANCO DE DADOS")
    print("=" * 60)
    
    db_path = 'instance/chamados.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(usuario);")
        colunas = cursor.fetchall()
        print(f"📋 Estrutura da tabela 'usuario':")
        for col in colunas:
            print(f"   - {col[1]} ({col[2]})")
        
        # Verificar todos os usuários
        cursor.execute("SELECT * FROM usuario;")
        usuarios = cursor.fetchall()
        print(f"\n👥 Usuários encontrados: {len(usuarios)}")
        
        for user in usuarios:
            print(f"\n   ID: {user[0]}")
            print(f"   Nome: {user[1]}")
            print(f"   Email: {user[2]}")
            print(f"   Senha (hash): {user[3][:50]}...")
            print(f"   Tipo: {user[4]}")
            
            # Testar senhas específicas
            senhas_teste = [
                "admin123",
                "admin", 
                "123",
                "password",
                "senha",
                "123456",
                user[2],  # email como senha
                "carsten",
                "empresa"
            ]
            
            senha_encontrada = False
            for senha in senhas_teste:
                try:
                    if check_password_hash(user[3], senha):
                        print(f"   ✅ SENHA ENCONTRADA: '{senha}'")
                        senha_encontrada = True
                        break
                except Exception as e:
                    print(f"   ❌ Erro ao verificar senha '{senha}': {e}")
            
            if not senha_encontrada:
                print(f"   ❌ Nenhuma senha válida encontrada")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_flask_direto():
    """Teste direto do Flask"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DIRETO DO FLASK")
    print("=" * 60)
    
    try:
        # Importar o app
        from app import app, db, Usuario
        from werkzeug.security import check_password_hash
        
        with app.app_context():
            # Verificar se o banco está acessível
            usuarios = Usuario.query.all()
            print(f"✅ Flask consegue acessar {len(usuarios)} usuários")
            
            # Testar login direto
            email_teste = "admin@empresa.com"
            senha_teste = "admin123"
            
            user = Usuario.query.filter_by(email=email_teste).first()
            if user:
                print(f"✅ Usuário encontrado: {user.nome}")
                if check_password_hash(user.senha, senha_teste):
                    print(f"✅ Senha válida para {email_teste}")
                else:
                    print(f"❌ Senha inválida para {email_teste}")
            else:
                print(f"❌ Usuário não encontrado: {email_teste}")
                
    except Exception as e:
        print(f"❌ ERRO no teste Flask: {e}")

def criar_usuario_teste():
    """Cria um usuário de teste simples"""
    print("\n" + "=" * 60)
    print("🔧 CRIANDO USUÁRIO DE TESTE")
    print("=" * 60)
    
    try:
        from app import app, db, Usuario
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Verificar se já existe
            user = Usuario.query.filter_by(email="teste@teste.com").first()
            if user:
                print("✅ Usuário de teste já existe")
                return True
            
            # Criar usuário de teste
            novo_user = Usuario()
            novo_user.nome = "Usuário Teste"
            novo_user.email = "teste@teste.com"
            novo_user.senha = generate_password_hash("123456")
            novo_user.tipo = "usuario"
            
            db.session.add(novo_user)
            db.session.commit()
            
            print("✅ Usuário de teste criado!")
            print("   Email: teste@teste.com")
            print("   Senha: 123456")
            
            return True
            
    except Exception as e:
        print(f"❌ ERRO ao criar usuário: {e}")
        return False

def main():
    """Função principal"""
    print("🔍 TESTE DETALHADO DO SISTEMA DE LOGIN")
    print("=" * 60)
    
    # Teste do banco
    testar_banco_detalhado()
    
    # Teste do Flask
    testar_flask_direto()
    
    # Criar usuário de teste
    criar_usuario_teste()
    
    print("\n" + "=" * 60)
    print("📝 RESUMO DOS TESTES")
    print("=" * 60)
    print("1. Verifique se o banco tem usuários válidos")
    print("2. Teste as credenciais encontradas")
    print("3. Se não funcionar, use o usuário de teste:")
    print("   Email: teste@teste.com")
    print("   Senha: 123456")
    print("4. Execute: python app.py")
    print("5. Acesse: http://localhost:5000")

if __name__ == "__main__":
    main() 