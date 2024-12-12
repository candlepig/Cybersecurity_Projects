import os
import base64
from cryptography.fernet import Fernet
import secrets
import string

# Generate a master key if it doesn't exist
def generate_key():
    if not os.path.exists("master.key"):
        key = Fernet.generate_key()
        with open("master.key", "wb") as key_file:
            key_file.write(key)

# Load the master key
def load_key():
    with open("master.key", "rb") as key_file:
        return key_file.read()

# Generate a secure password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Decrypt data
def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()

# Save a password to the file
def save_password(service, username, password, key):
    if os.path.exists("passwords.enc"):
        with open("passwords.enc", "rb") as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data, key)
    else:
        decrypted_data = ""

    # Append the new password
    decrypted_data += f"{service}|{username}|{password}\n"
    encrypted_data = encrypt_data(decrypted_data, key)

    with open("passwords.enc", "wb") as file:
        file.write(encrypted_data)

# View stored passwords
def view_passwords(key):
    if not os.path.exists("passwords.enc"):
        print("No passwords saved yet.")
        return

    with open("passwords.enc", "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = decrypt_data(encrypted_data, key)
    except Exception as e:
        print(f"Error decrypting data: {e}")
        return

    print("Stored Passwords:")
    for line in decrypted_data.strip().split("\n"):
        parts = line.split("|")
        if len(parts) != 3:
            print(f"Skipping malformed entry: {line}")
            continue
        service, username, password = parts
        print(f"Service: {service}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("-" * 20)
        
# Main program
def main():
    generate_key()
    key = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Generate and Save Password")
        print("2. View Passwords")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            length = int(input("Enter password length: "))
            password = generate_password(length)
            save_password(service, username, password, key)
            print(f"Generated password for {service}: {password}")
        elif choice == "2":
            view_passwords(key)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()