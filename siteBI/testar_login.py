#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar login com usuários existentes
"""

import sqlite3
from werkzeug.security import check_password_hash

def testar_usuarios_existentes():
    """Testa login com os usuários existentes no banco"""
    db_path = 'instance/chamados.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buscar todos os usuários
        cursor.execute("SELECT id, nome, email, senha, tipo FROM usuario;")
        usuarios = cursor.fetchall()
        
        print("🧪 TESTANDO LOGIN COM USUÁRIOS EXISTENTES")
        print("=" * 60)
        
        for user in usuarios:
            user_id, nome, email, senha_hash, tipo = user
            print(f"\n👤 Usuário: {nome}")
            print(f"   Email: {email}")
            print(f"   Tipo: {tipo}")
            print(f"   Hash da senha: {senha_hash[:50]}...")
            
            # Testar senhas comuns
            senhas_teste = [
                "admin",
                "admin123", 
                "123456",
                "password",
                "senha",
                "123",
                "admin@empresa.com",
                "guilherme.borges@carsten.com.br",
                "carsten",
                "empresa"
            ]
            
            senha_encontrada = False
            for senha in senhas_teste:
                if check_password_hash(senha_hash, senha):
                    print(f"   ✅ SENHA ENCONTRADA: '{senha}'")
                    senha_encontrada = True
                    break
            
            if not senha_encontrada:
                print(f"   ❌ Senha não identificada automaticamente")
                print(f"   💡 Tente usar o email como senha ou contate o administrador")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERRO: {e}")

def mostrar_credenciais_sugeridas():
    """Mostra credenciais sugeridas para teste"""
    print("\n" + "=" * 60)
    print("📝 CREDENCIAIS SUGERIDAS PARA TESTE:")
    print("=" * 60)
    print("1. Admin:")
    print("   Email: admin@empresa.com")
    print("   Senha: admin (ou admin123)")
    print()
    print("2. Usuário:")
    print("   Email: guilherme.borges@carsten.com.br")
    print("   Senha: guilherme.borges@carsten.com.br (ou carsten)")
    print()
    print("💡 DICAS:")
    print("- Tente usar o email como senha")
    print("- Tente senhas simples como 'admin', '123456'")
    print("- Se não funcionar, use a página de cadastro para criar um novo usuário")

if __name__ == "__main__":
    testar_usuarios_existentes()
    mostrar_credenciais_sugeridas() 