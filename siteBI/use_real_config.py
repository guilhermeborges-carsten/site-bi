#!/usr/bin/env python3
"""
Script para usar a configuração real criptografada temporariamente
"""

import os
import shutil

def use_real_config():
    print("🔐 Ativando configuração real criptografada...")
    
    # Verificar se existe backup
    if os.path.exists('config.py.backup'):
        print("📂 Backup encontrado!")
        
        # Fazer backup da configuração atual
        if os.path.exists('config.py'):
            shutil.copy('config.py', 'config.py.temp')
            print("💾 Backup temporário criado")
        
        # Copiar configuração real
        shutil.copy('config.py.backup', 'config.py')
        print("✅ Configuração real ativada!")
        
        print("\n🚀 Agora execute:")
        print("python app.py")
        print("\n⚠️  Para voltar à configuração segura:")
        print("python restore_safe_config.py")
        
    else:
        print("❌ Backup não encontrado!")
        print("🔐 Usando configuração criptografada...")
        
        # Tentar descriptografar
        try:
            from local_crypto import LocalCryptoManager
            crypto = LocalCryptoManager()
            
            if os.path.exists('config.encrypted'):
                print("🔓 Descriptografando configuração...")
                
                with open('config.encrypted', 'r', encoding='utf-8') as f:
                    encrypted_content = f.read()
                
                decrypted_content = crypto.decrypt_data(encrypted_content)
                
                # Fazer backup da configuração atual
                if os.path.exists('config.py'):
                    shutil.copy('config.py', 'config.py.temp')
                
                # Salvar configuração descriptografada
                with open('config.py', 'w', encoding='utf-8') as f:
                    f.write(decrypted_content)
                
                print("✅ Configuração descriptografada e ativada!")
                print("\n🚀 Agora execute:")
                print("python app.py")
                
            else:
                print("❌ Arquivo criptografado não encontrado!")
                
        except Exception as e:
            print(f"❌ Erro ao descriptografar: {str(e)}")

if __name__ == "__main__":
    use_real_config()
