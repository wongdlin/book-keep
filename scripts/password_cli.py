#!/usr/bin/env python3
"""
Password Management CLI Tool
Allows you to add, view, and manage encrypted passwords
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from password_manager import PasswordManager

def main():
    print("🔐 Password Management CLI")
    print("=" * 40)
    
    # Initialize password manager
    pm = PasswordManager()
    
    while True:
        print("\nOptions:")
        print("1. View all passwords")
        print("2. Add new password")
        print("3. View passwords by category")
        print("4. List categories")
        print("5. Test password decryption")
        print("6. Reset encryption system")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            view_all_passwords(pm)
        elif choice == "2":
            add_new_password(pm)
        elif choice == "3":
            view_by_category(pm)
        elif choice == "4":
            list_categories(pm)
        elif choice == "5":
            test_decryption(pm)
        elif choice == "6":
            reset_encryption(pm)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def view_all_passwords(pm):
    """View all decrypted passwords"""
    print("\n🔑 All Passwords:")
    passwords = pm.get_passwords()
    
    if not passwords:
        print("No passwords found.")
        return
    
    for i, password in enumerate(passwords, 1):
        print(f"  {i:2d}. {password}")

def add_new_password(pm):
    """Add a new password"""
    print("\n➕ Add New Password")
    
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    
    print("\nAvailable categories:")
    categories = pm.list_categories()
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print(f"  {len(categories) + 1}. Create new category")
    
    try:
        choice = int(input("Select category (number): "))
        if 1 <= choice <= len(categories):
            category = categories[choice - 1]
        elif choice == len(categories) + 1:
            category = input("Enter new category name: ").strip()
            if not category:
                print("Category name cannot be empty.")
                return
        else:
            print("Invalid choice.")
            return
        
        pm.add_password(password, category)
        print(f"✅ Password added to '{category}' category")
        
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"Error: {e}")

def view_by_category(pm):
    """View passwords by category"""
    print("\n📁 Passwords by Category")
    
    categories = pm.list_categories()
    if not categories:
        print("No categories found.")
        return
    
    for category in categories:
        passwords = pm.get_passwords_by_category(category)
        print(f"\n{category}:")
        if passwords:
            for i, password in enumerate(passwords, 1):
                print(f"  {i}. {password}")
        else:
            print("  No passwords in this category")

def list_categories(pm):
    """List all categories"""
    print("\n📂 Categories:")
    categories = pm.list_categories()
    
    if not categories:
        print("No categories found.")
        return
    
    for i, category in enumerate(categories, 1):
        count = len(pm.get_passwords_by_category(category))
        print(f"  {i}. {category} ({count} passwords)")

def test_decryption(pm):
    """Test password decryption"""
    print("\n🧪 Testing Password Decryption")
    
    # Show encrypted passwords from JSON
    try:
        with open(pm.passwords_file, 'r', encoding='utf-8') as f:
            import json
            data = json.load(f)
        
        print("Encrypted passwords in JSON file:")
        for category, encrypted_passwords in data.items():
            print(f"\n{category}:")
            for i, encrypted_pwd in enumerate(encrypted_passwords[:3], 1):  # Show first 3
                try:
                    decrypted = pm._decrypt_password(encrypted_pwd)
                    print(f"  {i}. {encrypted_pwd[:20]}... -> {decrypted}")
                except Exception as e:
                    print(f"  {i}. {encrypted_pwd[:20]}... -> Error: {e}")
        
        if any(len(encrypted_passwords) > 3 for encrypted_passwords in data.values()):
            print("  ... (showing first 3 of each category)")
            
    except Exception as e:
        print(f"Error reading encrypted passwords: {e}")

def reset_encryption(pm):
    """Reset the encryption system"""
    print("\n🔄 Reset Encryption System")
    print("⚠️  WARNING: This will delete all existing passwords and create a new encryption key!")
    
    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirm == "yes":
        pm.reset_encryption()
        print("✅ Encryption system has been reset")
    else:
        print("❌ Reset cancelled")

if __name__ == "__main__":
    main()
