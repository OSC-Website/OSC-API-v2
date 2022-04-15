import os
import binascii
import hashlib

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

async def encrypt_text(text : str) -> str:
    """
    Encrypts text 

    Parameters:
        text (str): The text you want to encrypt

    Returns:
        str: The hashed text
    """
    load_dotenv()
    SALT = (os.environ["SALT"]).encode()
    ITERATIONS = int(os.environ["ITERATIONS"])

    text = text.encode()

    encrypted = hashlib.pbkdf2_hmac("sha256", text, SALT, ITERATIONS)

    return binascii.hexlify(encrypted).decode()


async def encrypt_token(key : str, source : str) -> str:
    """
    Encrypts a text into an auth token

    Parameters:
        key (str): The key to use to encrypt the text
        source (str): The text you want to encrypt

    Returns:
        str: Source but encrypted
    """
    fernet = Fernet(key)
    encrypted = fernet.encrypt(source.encode())
    return encrypted.decode()


async def decrypt_token(key : str, source : str) -> str:
    """
    Decrypts an encrypted token into a username which will be used to get the user from the token

    Parameters:
        key (str): The key that was used to encrypt the text, this will reverse it
        source (str): The encrypted text you want to decrypt

    Returns:
        str: Source but encrypted
    """
    fernet = Fernet(key)
    decrypted = fernet.decrypt(source.encode())
    return decrypted.decode()