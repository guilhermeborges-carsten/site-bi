#!/usr/bin/env python3
"""
Script para restaurar a configuração segura
"""

import os
import shutil

def restore_safe_config():
    print("🛡️ Restaurando configuração segura...")
    
    # Verificar se existe backup temporário
    if os.path.exists('config.py.temp'):
        print("📂 Backup temporário encontrado!")
        
        # Restaurar configuração segura
        shutil.copy('config.py.temp', 'config.py')
        os.remove('config.py.temp')
        
        print("✅ Configuração segura restaurada!")
        print("🔐 Sistema agora usa configuração criptografada")
        
    else:
        print("⚠️  Backup temporário não encontrado")
        print("🔧 Criando configuração segura padrão...")
        
        # Criar configuração segura
        safe_config = '''# -*- coding: utf-8 -*-
"""
Configuração criptografada do Site BI
Para descriptografar, use: python use_real_config.py
"""

from local_crypto import decrypt_config

# Configuração criptografada (exemplo)
ENCRYPTED_CONFIG = """exemplo_criptografado"""

# Descriptografar a configuração
def get_decrypted_config():
    """Retorna a configuração descriptografada"""
    try:
        return decrypt_config(ENCRYPTED_CONFIG)
    except Exception as e:
        raise Exception(f"Erro ao descriptografar configuração: {str(e)}")
'''
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(safe_config)
        
        print("✅ Configuração segura criada!")
    
    print("\n🎯 Sistema seguro para produção!")
    print("📋 Para usar configuração real:")
    print("python use_real_config.py")

if __name__ == "__main__":
    restore_safe_config()
