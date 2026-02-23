import os
import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import PBKDF2

class SecurityManager:
    """Handles encryption and decryption of sensitive API keys."""
    
    def __init__(self, master_password: str, salt: bytes = None):
        if salt is None:
            self.salt = os.urandom(16)
        else:
            self.salt = salt
            
        # Derive a 32-byte key from password
        self.key = PBKDF2(master_password, self.salt, dkLen=32, count=100000)

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a string and returns base64 encoded ciphertext."""
        iv = os.urandom(16)
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
        
        # Combine salt, IV, and ciphertext
        combined = self.salt + iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')

    @classmethod
    def decrypt(cls, master_password: str, encrypted_data: str) -> str:
        """Decrypts base64 encoded encrypted data."""
        raw = base64.b64decode(encrypted_data)
        salt = raw[:16]
        iv = raw[16:32]
        ciphertext = raw[32:]
        
        # Re-derive the key with extracted salt
        key = PBKDF2(master_password, salt, dkLen=32, count=100000)
        
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(ciphertext).decode('utf-8')

# Example Usage (for testing)
if __name__ == "__main__":
    mgr = SecurityManager("supersecret")
    enc = mgr.encrypt("binance_api_secret_123")
    print(f"Encrypted: {enc}")
    dec = SecurityManager.decrypt("supersecret", enc)
    print(f"Decrypted: {dec}")
