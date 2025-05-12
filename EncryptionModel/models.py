from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from base64 import urlsafe_b64encode, urlsafe_b64decode

# Custom Django model field that encrypts text data when saving to the database
# and automatically decrypts it when loading from the database.
# Uses Fernet symmetric encryption to ensure data confidentiality.

#for retrive fernet key for encrypt and decrypt
fernet = Fernet(settings.FERNET_KEY)  

class EncryptedTextField(models.TextField):
    '''
    Custom Django TextField that automatically encrypts and decrypts its value using Fernet.

    '''
# This method is called before saving the value to the database.
# It encrypts the value using Fernet and encodes it in base64 to store as text.
    def get_prep_value(self, value) -> str: 
        if value is None:
            return value
        if isinstance(value, str):
            value = value.encode('utf-8')  # convert string to bytes
        encrypted_value = fernet.encrypt(value)  # encrypt the byte string
        return urlsafe_b64encode(encrypted_value).decode('utf-8')  # encode in base64 for DB storage

# This method is used when reading the value from the database.
# It decrypts the base64-encoded encrypted value and returns the original text.
    def from_db_value(self, value, expression, connection) -> str:
        if value is None:
            return value
        try:
            decrypted_value = fernet.decrypt(urlsafe_b64decode(value))  # decode from base64 then decrypt
            return decrypted_value.decode('utf-8')  # convert back to string
        except Exception:
            return value  # if decryption fails, return the raw value

# This method ensures that the value is correctly interpreted in Python code.
# It is used during model initialization and form handling.
    def to_python(self, value) -> str:
        if value is None:
            return value
        if isinstance(value, str):
            try:
                decrypted_value = fernet.decrypt(urlsafe_b64decode(value))  # attempt to decrypt
                return decrypted_value.decode('utf-8')  # return the original string
            except Exception:
                return value  # return as-is if not decryptable (already plain text or malformed)
        return value  # if not a string, just return the value as-is
    
class Message(models.Model):
    name = models.CharField(max_length=255)
    message = EncryptedTextField()
    
    def __str__(self):
        return self.name