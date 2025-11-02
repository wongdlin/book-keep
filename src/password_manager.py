import json
import base64
from pathlib import Path
from typing import List, Dict, Optional
from cryptography.fernet import Fernet
from config import Config

class PasswordManager:
    def __init__(self, passwords_file: Optional[str] = None, master_key_file: Optional[str] = None):
        self.passwords_file = Path(passwords_file) if passwords_file else Config.get_passwords_file()
        self.master_key_file = Path(master_key_file) if master_key_file else Config.get_master_key_file()
        self.cipher_suite = self._initialize_encryption()
        self.passwords = self.load_passwords()
    
    def _initialize_encryption(self):
        """Initialize encryption using master key"""
        if not self.master_key_file.exists():
            print("Creating new master key...")
            self._create_master_key()
        
        # Load master key
        with open(self.master_key_file, 'rb') as f:
            master_key = f.read()
        
        try:
            return Fernet(master_key)
        except ValueError:
            print("Invalid master key format. Creating new key...")
            self._create_master_key()
            with open(self.master_key_file, 'rb') as f:
                master_key = f.read()
            return Fernet(master_key)
    
    def _create_master_key(self):
        """Create a new master key for encryption"""
        key = Fernet.generate_key()
        
        with open(self.master_key_file, 'wb') as f:
            f.write(key)
        
        print(f"Master key created: {self.master_key_file}")
        print("⚠️  IMPORTANT: Keep this key file secure and backed up!")
    
    def reset_encryption(self):
        """Reset encryption system - creates new key and clears passwords"""
        print("🔄 Resetting encryption system...")
        
        # Remove existing files
        if self.master_key_file.exists():
            self.master_key_file.unlink()
            print("Removed old master key")
        
        if self.passwords_file.exists():
            self.passwords_file.unlink()
            print("Removed old passwords file")
        
        # Create new key
        self._create_master_key()
        
        # Reinitialize
        self.cipher_suite = self._initialize_encryption()
        self.passwords = self.load_passwords()
        
        print("✅ Encryption system reset successfully")
    
    def _encrypt_password(self, password: str) -> str:
        """Encrypt a single password"""
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return base64.b64encode(encrypted_password).decode()
    
    def _decrypt_password(self, encrypted_password: str) -> str:
        """Decrypt a single password"""
        encrypted_bytes = base64.b64decode(encrypted_password.encode())
        decrypted_password = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_password.decode()
    
    def load_passwords(self) -> List[str]:
        """Load and decrypt passwords from JSON file"""
        try:
            if not self.passwords_file.exists():
                print(f"Warning: {self.passwords_file} not found. Creating default encrypted file...")
                self.create_default_encrypted_passwords_file()
            
            with open(self.passwords_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Decrypt all passwords
            all_passwords = []
            for category, encrypted_passwords in data.items():
                if isinstance(encrypted_passwords, list):
                    for encrypted_pwd in encrypted_passwords:
                        try:
                            decrypted_pwd = self._decrypt_password(encrypted_pwd)
                            all_passwords.append(decrypted_pwd)
                        except Exception as e:
                            print(f"Warning: Could not decrypt password in {category}: {e}")
            
            print(f"Loaded {len(all_passwords)} encrypted passwords from {self.passwords_file}")
            return all_passwords
            
        except Exception as e:
            print(f"Error loading encrypted passwords: {e}")
            return []
    
    def create_default_encrypted_passwords_file(self):
        """Create a default encrypted passwords.json file"""
        default_passwords = {
            "common_passwords": [
                "password", "123456", "admin", "user", "1234", "12345",
                "qwerty", "abc123", "password123", "1234567890"
            ],
            "bank_passwords": [
                "bank123", "statement", "account", "finance"
            ],
            "document_passwords": [
                "document", "file", "secure", "private"
            ]
        }
        
        # Encrypt all passwords
        encrypted_data = {}
        for category, passwords in default_passwords.items():
            encrypted_data[category] = [self._encrypt_password(pwd) for pwd in passwords]
        
        with open(self.passwords_file, 'w', encoding='utf-8') as f:
            json.dump(encrypted_data, f, indent=2)
        
        print(f"Created encrypted {self.passwords_file}")
    
    def get_passwords(self) -> List[str]:
        """Get all passwords as a list"""
        return self.passwords
    
    def get_passwords_by_category(self, category: str) -> List[str]:
        """Get passwords from a specific category"""
        try:
            with open(self.passwords_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Decrypt and return passwords
            decrypted_passwords = []
            for encrypted_pwd in data.get(category, []):
                try:
                    decrypted_passwords.append(self._decrypt_password(encrypted_pwd))
                except Exception:
                    decrypted_passwords.append(encrypted_pwd)  # Return as is if decryption fails
            return decrypted_passwords
        except Exception as e:
            print(f"Error loading category {category}: {e}")
            return []
    
    def add_password(self, password: str, category: str = "custom"):
        """Add a new encrypted password to a category"""
        try:
            # Load existing data
            if self.passwords_file.exists():
                with open(self.passwords_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            
            if category not in data:
                data[category] = []
            
            # Encrypt the new password
            encrypted_password = self._encrypt_password(password)
            
            # Check if password already exists (compare encrypted versions)
            if encrypted_password not in data[category]:
                data[category].append(encrypted_password)
                
                # Save back to file
                with open(self.passwords_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                print(f"Added encrypted password to category '{category}'")
                # Reload passwords
                self.passwords = self.load_passwords()
            else:
                print(f"Password already exists in category '{category}'")
                
        except Exception as e:
            print(f"Error adding password: {e}")
    
    def list_categories(self) -> List[str]:
        """List all password categories"""
        try:
            with open(self.passwords_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return list(data.keys())
        except Exception as e:
            print(f"Error listing categories: {e}")
            return []
