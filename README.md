# Custom Model for Encrypted Fields

This Django project demonstrates how to create a custom model field that automatically encrypts and decrypts data using Fernet encryption from the `cryptography` library.

## Requirements

- Django
- cryptography: for encryption via Fernet
- python-dotenv: to load `.env` variables (for the Fernet key)
- faker: to generate fake data for testing (seeding)

## Setup

### 1. Create and activate a virtual environment

Use your preferred tool. For example, with pipenv:

```bash
pipenv shell
```

### 2. Install dependencies

```bash
pipenv install django
pipenv install cryptography
pipenv install python-dotenv
pipenv install faker
```

## Generate Fernet Key

To generate a Fernet key, run the following in a Python shell:

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

Copy the generated key and place it inside a `.env` file in the root directory of your project:

```
FERNET_KEY=your_generated_key_here
```

## Project Structure

### 1. Custom Encrypted Field

The core logic for the encrypted field is defined in:

```
EncryptionModel/models.py
```

Includes:

- `EncryptedTextField`: a custom Django field that handles encryption and decryption
- `Message`: a model with a name and an encrypted message field

### 2. Seeding Fake Data

To test the encrypted field, you can seed the database using a custom management command:

Location:

```
EncryptionModel/management/commands/seed_message.py
```

To run the command:

```bash
python manage.py seed_message
```

### 3. Management Command Structure

Make sure your app folder includes the following structure:

```
EncryptionModel/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── seed_message.py
```

This structure is required for Django to recognize and execute custom commands.

## Notes

- The encryption and decryption are handled automatically via the `EncryptedTextField`.
- Encrypted values are stored as base64-encoded strings in the database.
- The `.env` file must be present at the root of the project and loaded properly in `settings.py`.