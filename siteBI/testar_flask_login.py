#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar login no Flask
"""

import requests
import sys
import os

# Adicionar o diretório atual ao path para importar o app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_login_flask():
    """Testa o login via Flask"""
    
    # URL base (ajuste conforme necessário)
    base_url = "http://localhost:5000"
    
    # Credenciais conhecidas
    credenciais = [
        {
            "email": "admin@empresa.com",
            "senha": "admin123",
            "descricao": "Admin"
        },
        {
            "email": "guilherme.borges@carsten.com.br", 
            "senha": "123",
            "descricao": "Usuário Guilherme"
        }
    ]
    
    print("🧪 TESTANDO LOGIN NO FLASK")
    print("=" * 50)
    
    for cred in credenciais:
        print(f"\n👤 Testando: {cred['descricao']}")
        print(f"   Email: {cred['email']}")
        print(f"   Senha: {cred['senha']}")
        
        try:
            # Fazer requisição POST para login
            response = requests.post(
                f"{base_url}/login",
                data={
                    'email': cred['email'],
                    'senha': cred['senha']
                },
                allow_redirects=False,
                timeout=10
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 302:
                # Redirecionamento indica sucesso
                location = response.headers.get('Location', '')
                print(f"   ✅ Login bem-sucedido!")
                print(f"   🔗 Redirecionado para: {location}")
            else:
                print(f"   ❌ Login falhou")
                print(f"   📄 Conteúdo da resposta: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ ERRO: Não foi possível conectar ao servidor")
            print(f"   💡 Verifique se o Flask está rodando em {base_url}")
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
    
    print("\n" + "=" * 50)
    print("📝 INSTRUÇÕES:")
    print("1. Certifique-se de que o Flask está rodando:")
    print("   python app.py")
    print("2. Acesse: http://localhost:5000")
    print("3. Use as credenciais testadas acima")
    print("4. Verifique o console do Flask para logs de debug")

if __name__ == "__main__":
    testar_login_flask() 