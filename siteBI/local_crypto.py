# -*- coding: utf-8 -*-
"""
Sistema de criptografia local como alternativa à API externa
Pode ser facilmente substituído pela API quando estiver funcionando
"""

import base64
import hashlib
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class LocalCryptoManager:
    """Gerenciador de criptografia local usando AES"""
    
    def __init__(self, master_password="SiteBI2024"):
        """Inicializa com senha mestra padrão"""
        self.master_password = master_password.encode()
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self):
        """Deriva chave AES da senha mestra"""
        salt = b'sitebi_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password))
        return key
    
    def encrypt_data(self, data):
        """Criptografa dados (string ou dict)"""
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        encrypted_data = self.cipher.encrypt(data)
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_data(self, encrypted_data):
        """Descriptografa dados"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            
            # Tenta decodificar como JSON primeiro
            try:
                return json.loads(decrypted_data.decode('utf-8'))
            except json.JSONDecodeError:
                # Se não for JSON, retorna como string
                return decrypted_data.decode('utf-8')
                
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar: {str(e)}")
    
    def encrypt_file(self, file_path, output_path=None):
        """Criptografa um arquivo inteiro"""
        if output_path is None:
            output_path = file_path + '.encrypted'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encrypted_content = self.encrypt_data(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)
        
        return output_path
    
    def decrypt_file(self, file_path, output_path=None):
        """Descriptografa um arquivo inteiro"""
        if output_path is None:
            output_path = file_path.replace('.encrypted', '.decrypted')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()
        
        decrypted_content = self.decrypt_data(encrypted_content)
        
        if isinstance(decrypted_content, dict):
            # Se for um dict, salva como JSON formatado
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(decrypted_content, f, indent=2, ensure_ascii=False)
        else:
            # Se for string, salva como texto
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(decrypted_content)
        
        return output_path

# Funções auxiliares
def encrypt_config(config_data):
    """Criptografa configuração usando criptografia local"""
    crypto = LocalCryptoManager()
    return crypto.encrypt_data(config_data)

def decrypt_config(encrypted_config):
    """Descriptografa configuração usando criptografia local"""
    crypto = LocalCryptoManager()
    return crypto.decrypt_data(encrypted_config)

def encrypt_config_file(file_path, output_path=None):
    """Criptografa arquivo de configuração"""
    crypto = LocalCryptoManager()
    return crypto.encrypt_file(file_path, output_path)

def decrypt_config_file(file_path, output_path=None):
    """Descriptografa arquivo de configuração"""
    crypto = LocalCryptoManager()
    return crypto.decrypt_file(file_path, output_path)
