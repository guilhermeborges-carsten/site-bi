#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples do sistema
"""

def mostrar_credenciais():
    """Mostra as credenciais para teste"""
    print("🔑 CREDENCIAIS PARA LOGIN")
    print("=" * 40)
    print("1. Administrador:")
    print("   Email: admin@empresa.com")
    print("   Senha: admin123")
    print()
    print("2. Usuário:")
    print("   Email: guilherme.borges@carsten.com.br")
    print("   Senha: 123")
    print()
    print("3. Teste:")
    print("   Email: teste@teste.com")
    print("   Senha: 123456")
    print()
    print("🚀 INSTRUÇÕES:")
    print("=" * 40)
    print("1. Execute: python app.py")
    print("2. Acesse: http://localhost:5000")
    print("3. Use uma das credenciais acima")
    print()
    print("✅ Sistema revertido para versão simples!")

if __name__ == "__main__":
    mostrar_credenciais() 