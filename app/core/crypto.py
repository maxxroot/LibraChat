# app/core/crypto.py

import os, hashlib, hmac
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_pem, public_pem

def encrypt_message(public_key_pem, message):
    public_key = serialization.load_pem_public_key(public_key_pem)

    aes_key = os.urandom(32)

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return iv, encrypted_aes_key, ciphertext

def decrypt_message(private_key_pem, iv, encrypted_aes_key, ciphertext):
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_message.decode()

def verify_signature(public_key: str, signature: str, body: str, headers: dict):
    pass

def sign_request(private_key: str, body: str, headers: dict):
    pass