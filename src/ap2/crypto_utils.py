import json
import base64
import hashlib
import datetime
from typing import Any, Dict
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    """Generates an RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def get_private_key_pem(private_key) -> str:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

def get_public_key_pem(public_key) -> str:
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

def hash_object(obj: Any) -> str:
    """Generates a SHA-256 hash of a JSON-serializable object."""
    # Ensure canonical JSON representation
    canonical_json = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

def sign_cart_mandate(cart_contents_dict: Dict[str, Any], private_key_pem: str) -> str:
    """Signs cart contents with a merchant's private key using JWT."""
    payload = {
        "iss": "merchant_agent",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        "cart_hash": hash_object(cart_contents_dict)
    }
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    return token

def sign_payment_mandate(payment_contents_dict: Dict[str, Any], cart_mandate_hash: str, private_key_pem: str) -> str:
    """Signs a payment mandate and its associated cart mandate hash."""
    payload = {
        "iss": "user_device",
        "iat": datetime.datetime.utcnow(),
        "transaction_data": [
            cart_mandate_hash,
            hash_object(payment_contents_dict)
        ]
    }
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    return token
