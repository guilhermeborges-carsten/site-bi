#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criptografar config.py para deploy no Render
"""

import os
import shutil
from local_crypto import LocalCryptoManager

def main():
    print("🔐 Criptografando config.py para Render...")
    
    # Verificar se arquivos existem
    if not os.path.exists('config.py'):
        print("❌ config.py não encontrado!")
        return
    
    if not os.path.exists('local_crypto.py'):
        print("❌ local_crypto.py não encontrado!")
        return
    
    try:
        # Inicializar criptografia
        crypto = LocalCryptoManager()
        
        # Ler config.py atual
        with open('config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        print("📂 Configuração atual lida!")
        
        # Criptografar conteúdo
        encrypted_content = crypto.encrypt_data(config_content)
        
        # Salvar versão criptografada
        with open('config.py.encrypted', 'w', encoding='utf-8') as f:
            f.write(encrypted_content)
        
        print("✅ config.py.encrypted criado!")
        
        # Criar config.py seguro para GitHub
        safe_config = '''# -*- coding: utf-8 -*-
"""
Configuração segura para GitHub
A configuração real será descriptografada automaticamente no Render
"""

# Este arquivo será sobrescrito pelo start_render.py no Render
# Para desenvolvimento local, use: python use_real_config.py

from secure_config import config
'''
        
        # Fazer backup do config.py atual
        shutil.copy('config.py', 'config.py.backup')
        print("💾 Backup criado: config.py.backup")
        
        # Sobrescrever config.py com versão segura
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(safe_config)
        
        print("✅ config.py agora é seguro para GitHub!")
        
        print("\n🎯 Arquivos criados:")
        print("- config.py.encrypted (para Render)")
        print("- config.py.backup (para desenvolvimento local)")
        print("- config.py (versão segura para GitHub)")
        
        print("\n🚀 Para desenvolvimento local:")
        print("python use_real_config.py")
        
        print("\n🔒 Para GitHub (seguro):")
        print("git add .")
        print("git commit -m 'Configuração segura para Render'")
        print("git push origin main")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == '__main__':
    main()
