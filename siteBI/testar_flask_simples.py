#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para testar o Flask
"""

import webbrowser
import time
import os

def abrir_navegador():
    """Abre o navegador com as credenciais"""
    print("🌐 ABRINDO NAVEGADOR PARA TESTE")
    print("=" * 50)
    
    # Credenciais confirmadas
    credenciais = [
        {
            "tipo": "Administrador",
            "email": "admin@empresa.com",
            "senha": "admin123"
        },
        {
            "tipo": "Usuário",
            "email": "guilherme.borges@carsten.com.br", 
            "senha": "123"
        }
    ]
    
    print("📝 CREDENCIAIS PARA TESTE:")
    print("=" * 50)
    
    for i, cred in enumerate(credenciais, 1):
        print(f"{i}. {cred['tipo']}:")
        print(f"   Email: {cred['email']}")
        print(f"   Senha: {cred['senha']}")
        print()
    
    print("🚀 INSTRUÇÕES:")
    print("1. Certifique-se de que o Flask está rodando:")
    print("   python app.py")
    print()
    print("2. Acesse: http://localhost:5000")
    print()
    print("3. Use uma das credenciais acima")
    print()
    print("4. Se não funcionar, tente:")
    print("   - Verificar se não há espaços extras")
    print("   - Verificar se o Caps Lock está desligado")
    print("   - Usar a página de cadastro para criar novo usuário")
    
    # Aguardar um pouco e abrir o navegador
    print("\n⏳ Abrindo navegador em 3 segundos...")
    time.sleep(3)
    
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ Navegador aberto!")
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        print("💡 Abra manualmente: http://localhost:5000")

if __name__ == "__main__":
    abrir_navegador() 