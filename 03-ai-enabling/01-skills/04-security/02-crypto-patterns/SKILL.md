---
last_updated: 2026-02-25
status: active
name: crypto-patterns
description: Cryptography patterns - hashing, encryption, key management, TLS. Use for secure data handling.
triggers:
  files: ["**/crypto/**", "**/encryption/**", "**/security/**"]
  keywords: ["encryption", "hashing", "bcrypt", "AES", "RSA", "salt", "key management", "TLS", "certificate", "HMAC"]
allowed-tools: Read, Write, Edit
---

# Crypto Patterns Skill

Expert-level cryptographic patterns for secure software development. This skill covers password hashing, symmetric/asymmetric encryption, key management, TLS configuration, and cryptographic anti-patterns to avoid.

## Table of Contents

1. [Password Hashing](#password-hashing)
2. [Symmetric Encryption](#symmetric-encryption)
3. [Asymmetric Encryption](#asymmetric-encryption)
4. [Key Derivation](#key-derivation)
5. [Secure Random Generation](#secure-random-generation)
6. [Message Authentication (HMAC)](#message-authentication-hmac)
7. [Digital Signatures](#digital-signatures)
8. [TLS/SSL Configuration](#tlsssl-configuration)
9. [Certificate Management](#certificate-management)
10. [Secrets Management](#secrets-management)
11. [Envelope Encryption](#envelope-encryption)
12. [Cryptographic Anti-Patterns](#cryptographic-anti-patterns)

---


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Password Hashing

### Overview

Password hashing is a one-way function that transforms passwords into fixed-length strings. Proper password hashing uses:
- **Slow algorithms** (to resist brute force)
- **Salts** (to prevent rainbow table attacks)
- **Work factors** (to adjust computational cost over time)

### Recommended Algorithms

**Priority Order:**
1. **Argon2id** - Modern, memory-hard, resistant to GPU attacks
2. **bcrypt** - Industry standard, widely supported
3. **scrypt** - Memory-hard alternative
4. **PBKDF2** - Acceptable fallback (use high iterations)

### Argon2id (Best Choice)

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize hasher with secure defaults
ph = PasswordHasher(
    time_cost=2,          # Number of iterations
    memory_cost=65536,    # Memory usage in KB (64 MB)
    parallelism=4,        # Number of parallel threads
    hash_len=32,          # Length of hash in bytes
    salt_len=16           # Length of salt in bytes
)

# Hash password
def hash_password(password: str) -> str:
    """Hash a password using Argon2id."""
    return ph.hash(password)

# Verify password
def verify_password(hash: str, password: str) -> bool:
    """Verify password against Argon2id hash."""
    try:
        ph.verify(hash, password)

        # Check if rehashing needed (parameters changed)
        if ph.check_needs_rehash(hash):
            return True, hash_password(password)

        return True, None
    except VerifyMismatchError:
        return False, None

# Usage
hashed = hash_password("user_password_123")
is_valid, new_hash = verify_password(hashed, "user_password_123")
if new_hash:
    # Update stored hash with stronger parameters
    update_user_hash(user_id, new_hash)
```

```typescript
// Node.js with argon2
import argon2 from 'argon2';

// Hash password
async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,  // 64 MB
    timeCost: 3,
    parallelism: 4
  });
}

// Verify password
async function verifyPassword(hash: string, password: string): Promise<boolean> {
  try {
    return await argon2.verify(hash, password);
  } catch {
    return false;
  }
}

// Usage
const hash = await hashPassword('user_password_123');
const isValid = await verifyPassword(hash, 'user_password_123');
```

### bcrypt (Industry Standard)

```python
import bcrypt

# Hash password
def hash_password(password: str) -> str:
    """Hash password using bcrypt with work factor 12."""
    salt = bcrypt.gensalt(rounds=12)  # 2^12 iterations
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Verify password
def verify_password(hash: str, password: str) -> bool:
    """Verify password against bcrypt hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hash.encode('utf-8')
    )

# Adaptive work factor based on Moore's Law
import time

def get_work_factor(target_time_ms: float = 250.0) -> int:
    """Calculate optimal bcrypt work factor for target time."""
    password = b"benchmark_password"
    work_factor = 10

    while work_factor < 16:
        salt = bcrypt.gensalt(rounds=work_factor)
        start = time.time()
        bcrypt.hashpw(password, salt)
        elapsed_ms = (time.time() - start) * 1000

        if elapsed_ms >= target_time_ms:
            return work_factor
        work_factor += 1

    return 16  # Maximum reasonable work factor

# Usage
optimal_rounds = get_work_factor(target_time_ms=250)
print(f"Optimal work factor: {optimal_rounds}")
```

```go
// Go with bcrypt
package auth

import (
    "golang.org/x/crypto/bcrypt"
)

// Hash password with bcrypt
func HashPassword(password string) (string, error) {
    hash, err := bcrypt.GenerateFromPassword(
        []byte(password),
        bcrypt.DefaultCost, // Cost 10 (2^10 iterations)
    )
    if err != nil {
        return "", err
    }
    return string(hash), nil
}

// Verify password
func VerifyPassword(hash, password string) bool {
    err := bcrypt.CompareHashAndPassword(
        []byte(hash),
        []byte(password),
    )
    return err == nil
}

// Custom cost for specific security requirements
func HashPasswordWithCost(password string, cost int) (string, error) {
    if cost < bcrypt.MinCost || cost > bcrypt.MaxCost {
        cost = bcrypt.DefaultCost
    }

    hash, err := bcrypt.GenerateFromPassword(
        []byte(password),
        cost,
    )
    if err != nil {
        return "", err
    }
    return string(hash), nil
}
```

### PBKDF2 (Fallback)

```python
import hashlib
import os
from base64 import b64encode, b64decode

def hash_password_pbkdf2(password: str, iterations: int = 600000) -> str:
    """Hash password using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=32
    )

    # Store as: algorithm$iterations$salt$hash
    return f"pbkdf2_sha256${iterations}${b64encode(salt).decode()}${b64encode(key).decode()}"

def verify_password_pbkdf2(stored_hash: str, password: str) -> bool:
    """Verify password against PBKDF2 hash."""
    try:
        algorithm, iterations, salt_b64, hash_b64 = stored_hash.split('$')
        iterations = int(iterations)
        salt = b64decode(salt_b64)
        stored_key = b64decode(hash_b64)

        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations,
            dklen=32
        )

        # Constant-time comparison
        return compare_digest(stored_key, new_key)
    except Exception:
        return False

from hmac import compare_digest
```

### Password Hashing Best Practices

**Configuration Guidelines:**

| Algorithm | Work Factor | Memory | Time Target | Use Case |
|-----------|-------------|---------|-------------|----------|
| Argon2id | time=2, mem=64MB | 64 MB | 250-500ms | New projects (best) |
| bcrypt | rounds=12-14 | ~4 KB | 250-500ms | Standard apps |
| scrypt | N=32768, r=8, p=1 | 256 MB | 250-500ms | High-security apps |
| PBKDF2 | 600,000+ | Minimal | 250-500ms | Legacy compatibility |

**Implementation Checklist:**

```python
# ✅ DO: Use proper password hashing
def register_user(username: str, password: str):
    # 1. Validate password strength
    if not is_strong_password(password):
        raise ValueError("Password too weak")

    # 2. Hash with proper algorithm
    hashed = hash_password(password)

    # 3. Store only the hash (never plaintext)
    db.save_user(username, hashed)

# ✅ DO: Verify with constant-time comparison (built into libraries)
def login_user(username: str, password: str):
    user = db.get_user(username)
    if not user:
        # Prevent timing attacks: hash dummy password
        hash_password("dummy_password_to_prevent_timing")
        return False

    return verify_password(user.password_hash, password)

# ❌ DON'T: Roll your own hashing
def bad_hash(password: str) -> str:
    # NEVER DO THIS - not secure!
    return hashlib.sha256(password.encode()).hexdigest()

# ❌ DON'T: Use weak algorithms
import md5  # Never for passwords!
import sha1  # Never for passwords!

# ❌ DON'T: Hash without salt
def bad_hash_no_salt(password: str) -> str:
    # Vulnerable to rainbow tables
    return hashlib.sha256(password.encode()).hexdigest()

# ❌ DON'T: Use fast hashing algorithms
def bad_hash_fast(password: str) -> str:
    # Too fast = vulnerable to brute force
    return hashlib.sha256(password.encode()).hexdigest()
```

**Pepper Pattern (Additional Layer):**

```python
import os
from typing import Optional

# Store pepper in environment variable (separate from database)
PEPPER = os.getenv("PASSWORD_PEPPER", "")

def hash_password_with_pepper(password: str) -> str:
    """Add pepper to password before hashing."""
    peppered = password + PEPPER
    return hash_password(peppered)

def verify_password_with_pepper(hash: str, password: str) -> bool:
    """Verify password with pepper."""
    peppered = password + PEPPER
    return verify_password(hash, peppered)

# Pepper rotation pattern
def rotate_pepper(
    user_id: int,
    password: str,
    old_pepper: str,
    new_pepper: str
):
    """Migrate user to new pepper on next login."""
    # 1. Verify with old pepper
    old_peppered = password + old_pepper
    user = db.get_user(user_id)

    if not verify_password(user.password_hash, old_peppered):
        return False

    # 2. Rehash with new pepper
    new_peppered = password + new_pepper
    new_hash = hash_password(new_peppered)

    # 3. Update database
    db.update_user_hash(user_id, new_hash)
    return True
```

---

## Symmetric Encryption

### Overview

Symmetric encryption uses the same key for encryption and decryption. Modern symmetric encryption uses:
- **AES** (Advanced Encryption Standard)
- **Authenticated modes** (GCM, CCM) to prevent tampering
- **Unique IVs/nonces** for each encryption

### AES-GCM (Recommended)

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import os
import json
from base64 import b64encode, b64decode

class AESGCMCipher:
    """AES-GCM encryption with proper IV handling."""

    def __init__(self, key: bytes = None):
        """Initialize cipher with 256-bit key."""
        self.key = key or AESGCM.generate_key(bit_length=256)
        self.cipher = AESGCM(self.key)

    def encrypt(self, plaintext: bytes, associated_data: bytes = None) -> str:
        """Encrypt data with AES-GCM."""
        # Generate unique nonce (NEVER reuse with same key)
        nonce = os.urandom(12)  # 96 bits for GCM

        # Encrypt with authentication
        ciphertext = self.cipher.encrypt(
            nonce,
            plaintext,
            associated_data
        )

        # Return nonce + ciphertext (nonce is not secret)
        result = {
            'nonce': b64encode(nonce).decode(),
            'ciphertext': b64encode(ciphertext).decode(),
            'aad': b64encode(associated_data).decode() if associated_data else None
        }
        return json.dumps(result)

    def decrypt(self, encrypted_data: str) -> bytes:
        """Decrypt AES-GCM data."""
        data = json.loads(encrypted_data)
        nonce = b64decode(data['nonce'])
        ciphertext = b64decode(data['ciphertext'])
        aad = b64decode(data['aad']) if data['aad'] else None

        # Decrypt and verify authentication tag
        try:
            plaintext = self.cipher.decrypt(nonce, ciphertext, aad)
            return plaintext
        except Exception as e:
            raise ValueError("Decryption failed - data tampered or wrong key") from e

# Usage
cipher = AESGCMCipher()
key = cipher.key  # Save this securely

# Encrypt
plaintext = b"Sensitive user data"
associated_data = b"user_id:12345"  # Authenticated but not encrypted
encrypted = cipher.encrypt(plaintext, associated_data)

# Decrypt
decrypted = cipher.decrypt(encrypted)
assert decrypted == plaintext
```

```typescript
// Node.js with crypto module
import crypto from 'crypto';

interface EncryptedData {
  iv: string;
  ciphertext: string;
  authTag: string;
  aad?: string;
}

class AESGCMCipher {
  private key: Buffer;

  constructor(key?: Buffer) {
    // 256-bit key
    this.key = key || crypto.randomBytes(32);
  }

  encrypt(plaintext: string, associatedData?: string): string {
    // Generate unique IV (96 bits for GCM)
    const iv = crypto.randomBytes(12);

    // Create cipher
    const cipher = crypto.createCipheriv('aes-256-gcm', this.key, iv);

    // Add associated data if provided
    if (associatedData) {
      cipher.setAAD(Buffer.from(associatedData), {
        plaintextLength: Buffer.byteLength(plaintext)
      });
    }

    // Encrypt
    let ciphertext = cipher.update(plaintext, 'utf8', 'base64');
    ciphertext += cipher.final('base64');

    // Get authentication tag
    const authTag = cipher.getAuthTag();

    // Return IV + ciphertext + tag
    const result: EncryptedData = {
      iv: iv.toString('base64'),
      ciphertext,
      authTag: authTag.toString('base64'),
      aad: associatedData
    };

    return JSON.stringify(result);
  }

  decrypt(encryptedData: string): string {
    const data: EncryptedData = JSON.parse(encryptedData);
    const iv = Buffer.from(data.iv, 'base64');
    const authTag = Buffer.from(data.authTag, 'base64');

    // Create decipher
    const decipher = crypto.createDecipheriv('aes-256-gcm', this.key, iv);
    decipher.setAuthTag(authTag);

    // Add associated data if present
    if (data.aad) {
      decipher.setAAD(Buffer.from(data.aad));
    }

    // Decrypt
    let plaintext = decipher.update(data.ciphertext, 'base64', 'utf8');
    plaintext += decipher.final('utf8');

    return plaintext;
  }

  getKey(): string {
    return this.key.toString('base64');
  }
}

// Usage
const cipher = new AESGCMCipher();
const encrypted = cipher.encrypt('Sensitive data', 'user_id:12345');
const decrypted = cipher.decrypt(encrypted);
```

### ChaCha20-Poly1305 (Alternative to AES)

```python
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
from base64 import b64encode, b64decode

class ChaCha20Cipher:
    """ChaCha20-Poly1305 - faster than AES on devices without AES-NI."""

    def __init__(self, key: bytes = None):
        self.key = key or ChaCha20Poly1305.generate_key()
        self.cipher = ChaCha20Poly1305(self.key)

    def encrypt(self, plaintext: bytes, associated_data: bytes = None) -> dict:
        nonce = os.urandom(12)  # 96-bit nonce
        ciphertext = self.cipher.encrypt(nonce, plaintext, associated_data)

        return {
            'nonce': b64encode(nonce).decode(),
            'ciphertext': b64encode(ciphertext).decode()
        }

    def decrypt(self, encrypted: dict) -> bytes:
        nonce = b64decode(encrypted['nonce'])
        ciphertext = b64decode(encrypted['ciphertext'])

        return self.cipher.decrypt(nonce, ciphertext, None)

# Usage: Same interface as AES-GCM
cipher = ChaCha20Cipher()
encrypted = cipher.encrypt(b"Data")
decrypted = cipher.decrypt(encrypted)
```

### File Encryption Pattern

```python
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_file(
    input_path: Path,
    output_path: Path,
    key: bytes,
    chunk_size: int = 64 * 1024  # 64 KB chunks
):
    """Encrypt large file in chunks."""
    cipher = AESGCM(key)
    nonce = os.urandom(12)

    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        # Write nonce first
        outfile.write(nonce)

        # Encrypt in chunks
        chunk_num = 0
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break

            # Use chunk number as additional data (prevents reordering)
            aad = str(chunk_num).encode()
            encrypted_chunk = cipher.encrypt(nonce, chunk, aad)

            # Write chunk size then chunk
            outfile.write(len(encrypted_chunk).to_bytes(4, 'big'))
            outfile.write(encrypted_chunk)

            chunk_num += 1

            # Generate new nonce for each chunk (important!)
            nonce = os.urandom(12)
            outfile.write(nonce)

def decrypt_file(
    input_path: Path,
    output_path: Path,
    key: bytes
):
    """Decrypt large file in chunks."""
    cipher = AESGCM(key)

    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        chunk_num = 0

        # Read first nonce
        nonce = infile.read(12)

        while True:
            # Read chunk size
            size_bytes = infile.read(4)
            if not size_bytes:
                break

            chunk_size = int.from_bytes(size_bytes, 'big')
            encrypted_chunk = infile.read(chunk_size)

            # Decrypt
            aad = str(chunk_num).encode()
            decrypted_chunk = cipher.decrypt(nonce, encrypted_chunk, aad)
            outfile.write(decrypted_chunk)

            chunk_num += 1

            # Read next nonce
            nonce = infile.read(12)
            if len(nonce) < 12:
                break

# Usage
key = AESGCM.generate_key(bit_length=256)
encrypt_file(Path("document.pdf"), Path("document.pdf.enc"), key)
decrypt_file(Path("document.pdf.enc"), Path("document.pdf"), key)
```

### Symmetric Encryption Best Practices

**Algorithm Selection:**

| Algorithm | Use Case | Performance | Security |
|-----------|----------|-------------|----------|
| AES-256-GCM | General purpose, hardware acceleration | Fast with AES-NI | Excellent |
| ChaCha20-Poly1305 | Mobile, IoT, no AES-NI | Fast on all devices | Excellent |
| AES-256-CBC | Legacy systems (avoid for new) | Fast | Good (needs HMAC) |

**Key Requirements:**

```python
# ✅ DO: Generate cryptographically secure keys
import secrets

def generate_key(key_size: int = 32) -> bytes:
    """Generate 256-bit encryption key."""
    return secrets.token_bytes(key_size)

# ✅ DO: Use unique IVs/nonces
def get_unique_nonce() -> bytes:
    """Generate unique nonce (NEVER reuse!)."""
    return os.urandom(12)  # 96 bits for GCM

# ✅ DO: Use authenticated encryption
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
cipher = AESGCM(key)
ciphertext = cipher.encrypt(nonce, plaintext, associated_data)

# ❌ DON'T: Use unauthenticated modes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# CBC without HMAC = vulnerable to padding oracle attacks
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

# ❌ DON'T: Reuse nonces
nonce = os.urandom(12)
ciphertext1 = cipher.encrypt(nonce, data1, None)
ciphertext2 = cipher.encrypt(nonce, data2, None)  # DANGEROUS!

# ❌ DON'T: Use weak key sizes
key = os.urandom(16)  # 128-bit is minimum, use 256-bit
```

---

## Asymmetric Encryption

### Overview

Asymmetric encryption uses a public key (for encryption) and private key (for decryption). Use cases:
- **Key exchange** (ECDH, RSA-OAEP)
- **Digital signatures** (RSA-PSS, ECDSA, EdDSA)
- **Hybrid encryption** (asymmetric key exchange + symmetric data encryption)

### RSA Encryption

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os

class RSACipher:
    """RSA encryption with OAEP padding."""

    def __init__(self, key_size: int = 4096):
        """Generate RSA key pair."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size  # 4096 bits for long-term security
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt with RSA-OAEP."""
        # Max plaintext size = key_size/8 - 2*hash_size - 2
        # For 4096-bit key with SHA256: ~446 bytes
        ciphertext = self.public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """Decrypt with RSA-OAEP."""
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    def export_public_key(self) -> bytes:
        """Export public key in PEM format."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def export_private_key(self, password: bytes = None) -> bytes:
        """Export private key in PEM format (encrypted)."""
        encryption_algorithm = (
            serialization.BestAvailableEncryption(password)
            if password
            else serialization.NoEncryption()
        )

        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )

    @classmethod
    def load_public_key(cls, pem_data: bytes):
        """Load public key from PEM."""
        instance = cls.__new__(cls)
        instance.public_key = serialization.load_pem_public_key(pem_data)
        return instance

    @classmethod
    def load_private_key(cls, pem_data: bytes, password: bytes = None):
        """Load private key from PEM."""
        instance = cls.__new__(cls)
        instance.private_key = serialization.load_pem_private_key(
            pem_data,
            password=password
        )
        instance.public_key = instance.private_key.public_key()
        return instance

# Usage
rsa_cipher = RSACipher(key_size=4096)

# Encrypt (anyone with public key)
ciphertext = rsa_cipher.encrypt(b"Secret message")

# Decrypt (only holder of private key)
plaintext = rsa_cipher.decrypt(ciphertext)

# Export keys
public_pem = rsa_cipher.export_public_key()
private_pem = rsa_cipher.export_private_key(password=b"strong_password")

# Load keys later
loaded_cipher = RSACipher.load_private_key(private_pem, password=b"strong_password")
```

### Elliptic Curve Encryption (ECIES)

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class ECIESCipher:
    """Elliptic Curve Integrated Encryption Scheme."""

    def __init__(self, curve=ec.SECP384R1()):
        """Generate EC key pair."""
        self.private_key = ec.generate_private_key(curve)
        self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext: bytes, recipient_public_key: ec.EllipticCurvePublicKey) -> dict:
        """Encrypt using ECIES (ephemeral ECDH + AES-GCM)."""
        # 1. Generate ephemeral key pair
        ephemeral_private = ec.generate_private_key(ec.SECP384R1())
        ephemeral_public = ephemeral_private.public_key()

        # 2. Perform ECDH to get shared secret
        shared_key = ephemeral_private.exchange(
            ec.ECDH(),
            recipient_public_key
        )

        # 3. Derive encryption key from shared secret
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ecies-encryption'
        ).derive(shared_key)

        # 4. Encrypt plaintext with AES-GCM
        cipher = AESGCM(derived_key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, plaintext, None)

        # 5. Return ephemeral public key + encrypted data
        return {
            'ephemeral_public_key': ephemeral_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ),
            'nonce': nonce,
            'ciphertext': ciphertext
        }

    def decrypt(self, encrypted_data: dict) -> bytes:
        """Decrypt ECIES encrypted data."""
        # 1. Load ephemeral public key
        ephemeral_public = serialization.load_pem_public_key(
            encrypted_data['ephemeral_public_key']
        )

        # 2. Perform ECDH with our private key
        shared_key = self.private_key.exchange(
            ec.ECDH(),
            ephemeral_public
        )

        # 3. Derive same encryption key
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ecies-encryption'
        ).derive(shared_key)

        # 4. Decrypt with AES-GCM
        cipher = AESGCM(derived_key)
        plaintext = cipher.decrypt(
            encrypted_data['nonce'],
            encrypted_data['ciphertext'],
            None
        )

        return plaintext

# Usage
alice = ECIESCipher()
bob = ECIESCipher()

# Alice encrypts for Bob
encrypted = alice.encrypt(b"Secret message", bob.public_key)

# Bob decrypts with his private key
plaintext = bob.decrypt(encrypted)
```

### Hybrid Encryption (Best Practice)

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import os
from base64 import b64encode, b64decode
import json

class HybridCipher:
    """
    Hybrid encryption: RSA for key exchange + AES-GCM for data.

    Best of both worlds:
    - RSA: Secure key exchange
    - AES: Fast bulk encryption
    """

    def __init__(self, rsa_key_size: int = 4096):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=rsa_key_size
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext: bytes, recipient_public_key: rsa.RSAPublicKey) -> str:
        """Hybrid encrypt: Generate AES key, encrypt data, wrap key with RSA."""
        # 1. Generate random AES key
        aes_key = AESGCM.generate_key(bit_length=256)

        # 2. Encrypt data with AES-GCM
        cipher = AESGCM(aes_key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, plaintext, None)

        # 3. Encrypt AES key with RSA (key wrapping)
        wrapped_key = recipient_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 4. Return all components
        result = {
            'wrapped_key': b64encode(wrapped_key).decode(),
            'nonce': b64encode(nonce).decode(),
            'ciphertext': b64encode(ciphertext).decode()
        }
        return json.dumps(result)

    def decrypt(self, encrypted_data: str) -> bytes:
        """Hybrid decrypt: Unwrap AES key with RSA, decrypt data with AES."""
        data = json.loads(encrypted_data)

        # 1. Decrypt AES key with RSA (key unwrapping)
        wrapped_key = b64decode(data['wrapped_key'])
        aes_key = self.private_key.decrypt(
            wrapped_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 2. Decrypt data with AES-GCM
        cipher = AESGCM(aes_key)
        nonce = b64decode(data['nonce'])
        ciphertext = b64decode(data['ciphertext'])
        plaintext = cipher.decrypt(nonce, ciphertext, None)

        return plaintext

# Usage - Best for large data
alice = HybridCipher()
bob = HybridCipher()

# Alice encrypts 10MB file for Bob
large_data = b"X" * (10 * 1024 * 1024)  # 10 MB
encrypted = alice.encrypt(large_data, bob.public_key)

# Bob decrypts
plaintext = bob.decrypt(encrypted)
```

---

## Key Derivation

### Overview

Key derivation functions (KDFs) generate cryptographic keys from passwords or other key material. Use cases:
- Deriving multiple keys from one master key
- Converting passwords to encryption keys
- Key stretching for password-based encryption

### HKDF (HMAC-based KDF)

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

def derive_keys(master_key: bytes, salt: bytes = None, num_keys: int = 3) -> list[bytes]:
    """Derive multiple keys from master key using HKDF."""
    if salt is None:
        salt = os.urandom(32)

    keys = []
    for i in range(num_keys):
        # Use different info for each key
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit keys
            salt=salt,
            info=f"key-{i}".encode()
        )
        key = hkdf.derive(master_key)
        keys.append(key)

    return keys

# Usage: Derive encryption key, MAC key, and signing key from master
master_key = os.urandom(32)
encryption_key, mac_key, signing_key = derive_keys(master_key)
```

### Password-Based KDF (PBKDF2)

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os

def derive_key_from_password(
    password: str,
    salt: bytes = None,
    iterations: int = 600000
) -> tuple[bytes, bytes]:
    """Derive encryption key from password."""
    if salt is None:
        salt = os.urandom(32)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )

    key = kdf.derive(password.encode('utf-8'))
    return key, salt

# Usage: Password-based encryption
password = "user_password_123"
key, salt = derive_key_from_password(password)

# Save salt with ciphertext (salt is not secret)
# Later: Use same password and salt to derive same key
```

### Scrypt (Memory-Hard KDF)

```python
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os

def derive_key_scrypt(
    password: str,
    salt: bytes = None,
    n: int = 2**14,     # CPU/memory cost (16384)
    r: int = 8,          # Block size
    p: int = 1           # Parallelization
) -> tuple[bytes, bytes]:
    """Derive key using memory-hard scrypt."""
    if salt is None:
        salt = os.urandom(32)

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=n,
        r=r,
        p=p
    )

    key = kdf.derive(password.encode('utf-8'))
    return key, salt

# Usage: More resistant to hardware attacks than PBKDF2
password = "user_password_123"
key, salt = derive_key_scrypt(password)
```

---

## Secure Random Generation

### Overview

Cryptographic operations require high-quality randomness. NEVER use standard random generators (`random.random()`) for security.

### Secure Random Patterns

```python
import secrets  # Python's cryptographic RNG
import os

# ✅ DO: Use secrets module
def generate_token(length: int = 32) -> str:
    """Generate URL-safe token."""
    return secrets.token_urlsafe(length)

def generate_key(length: int = 32) -> bytes:
    """Generate encryption key."""
    return secrets.token_bytes(length)

def generate_hex_token(length: int = 32) -> str:
    """Generate hex token."""
    return secrets.token_hex(length)

# ✅ DO: Use os.urandom for bytes
def generate_random_bytes(length: int) -> bytes:
    """Generate random bytes from OS entropy."""
    return os.urandom(length)

# ✅ DO: Secure random integers
def generate_random_int(min_val: int, max_val: int) -> int:
    """Generate random integer in range."""
    return secrets.randbelow(max_val - min_val + 1) + min_val

# ✅ DO: Secure random choice
def choose_random_item(items: list):
    """Randomly select item from list."""
    return secrets.choice(items)

# ❌ DON'T: Use standard random module
import random
random_value = random.random()  # NOT cryptographically secure!
random_int = random.randint(0, 100)  # NOT secure!

# ❌ DON'T: Use timestamp-based "randomness"
import time
bad_random = int(time.time() * 1000)  # Predictable!

# ❌ DON'T: Use incremental values
counter = 0
def bad_token():
    global counter
    counter += 1
    return f"token_{counter}"  # Guessable!
```

### Secure Session Token Generation

```python
import secrets
import hashlib
from datetime import datetime, timedelta

class SessionTokenManager:
    """Secure session token management."""

    @staticmethod
    def generate_token() -> str:
        """Generate cryptographically secure session token."""
        # 256 bits of entropy
        return secrets.token_urlsafe(32)

    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def generate_api_key() -> str:
        """Generate API key with prefix."""
        prefix = "sk"  # Secret key prefix
        random_part = secrets.token_urlsafe(32)
        return f"{prefix}_{random_part}"

    @staticmethod
    def hash_token(token: str) -> str:
        """Hash token for storage (store hash, not plaintext)."""
        return hashlib.sha256(token.encode()).hexdigest()

# Usage
session_token = SessionTokenManager.generate_token()
token_hash = SessionTokenManager.hash_token(session_token)

# Store token_hash in database, return session_token to user
# Later: Hash incoming token and compare with stored hash
```

---

## Message Authentication (HMAC)

### Overview

HMAC (Hash-based Message Authentication Code) provides message integrity and authenticity. It proves:
1. Message hasn't been tampered with
2. Message came from holder of secret key

### HMAC Patterns

```python
import hmac
import hashlib
import secrets

class HMACAuthenticator:
    """HMAC message authentication."""

    def __init__(self, key: bytes = None):
        """Initialize with secret key."""
        self.key = key or secrets.token_bytes(32)

    def sign(self, message: bytes) -> bytes:
        """Generate HMAC signature."""
        return hmac.new(
            self.key,
            message,
            hashlib.sha256
        ).digest()

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify HMAC signature (constant-time comparison)."""
        expected_signature = self.sign(message)
        return hmac.compare_digest(expected_signature, signature)

    def sign_message(self, message: bytes) -> tuple[bytes, bytes]:
        """Return message with signature."""
        signature = self.sign(message)
        return message, signature

    def verify_message(self, message: bytes, signature: bytes) -> bool:
        """Verify message authenticity."""
        return self.verify(message, signature)

# Usage
authenticator = HMACAuthenticator()

# Sign message
message = b"Transfer $1000 from Alice to Bob"
signature = authenticator.sign(message)

# Verify message
is_valid = authenticator.verify(message, signature)

# Tampered message fails verification
tampered = b"Transfer $9999 from Alice to Bob"
is_valid = authenticator.verify(tampered, signature)  # False
```

### Webhook Signature Verification

```python
import hmac
import hashlib
from fastapi import Request, HTTPException

class WebhookVerifier:
    """Verify webhook signatures (e.g., GitHub, Stripe)."""

    def __init__(self, secret: str):
        self.secret = secret.encode()

    async def verify_request(self, request: Request, signature_header: str):
        """Verify webhook request signature."""
        body = await request.body()

        # Calculate expected signature
        expected_signature = hmac.new(
            self.secret,
            body,
            hashlib.sha256
        ).hexdigest()

        # Get signature from header (format: "sha256=...")
        if not signature_header.startswith('sha256='):
            raise HTTPException(status_code=401, detail="Invalid signature format")

        received_signature = signature_header[7:]  # Remove "sha256=" prefix

        # Constant-time comparison
        if not hmac.compare_digest(expected_signature, received_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        return True

# Usage in FastAPI
from fastapi import FastAPI, Header

app = FastAPI()
verifier = WebhookVerifier(secret="webhook_secret")

@app.post("/webhook")
async def handle_webhook(
    request: Request,
    x_signature: str = Header(..., alias="X-Hub-Signature-256")
):
    await verifier.verify_request(request, x_signature)
    # Process webhook...
    return {"status": "ok"}
```

---

## Digital Signatures

### Overview

Digital signatures provide:
- **Authentication** - Proves who signed the message
- **Non-repudiation** - Signer cannot deny signing
- **Integrity** - Detects tampering

### RSA-PSS Signatures

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class RSASignature:
    """RSA digital signatures with PSS padding."""

    def __init__(self, key_size: int = 4096):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        self.public_key = self.private_key.public_key()

    def sign(self, message: bytes) -> bytes:
        """Sign message with RSA-PSS."""
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify RSA-PSS signature."""
        try:
            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

# Usage
signer = RSASignature()

# Sign document
document = b"Contract terms..."
signature = signer.sign(document)

# Verify signature
is_valid = signer.verify(document, signature)

# Export public key for verification
public_pem = signer.public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
```

### EdDSA (Ed25519) Signatures

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

class Ed25519Signature:
    """Ed25519 signatures - faster and smaller than RSA."""

    def __init__(self):
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, message: bytes) -> bytes:
        """Sign message with Ed25519 (deterministic)."""
        return self.private_key.sign(message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify Ed25519 signature."""
        try:
            self.public_key.verify(signature, message)
            return True
        except InvalidSignature:
            return False

    def export_public_key(self) -> bytes:
        """Export public key (32 bytes)."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def export_private_key(self) -> bytes:
        """Export private key (32 bytes)."""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )

# Usage - Much faster than RSA
signer = Ed25519Signature()

message = b"Authenticate this action"
signature = signer.sign(message)  # 64 bytes
is_valid = signer.verify(message, signature)
```

---

## TLS/SSL Configuration

### Overview

Transport Layer Security (TLS) encrypts data in transit. Modern TLS configuration requires:
- TLS 1.2+ only (disable SSLv3, TLS 1.0, TLS 1.1)
- Strong cipher suites
- Perfect Forward Secrecy (PFS)
- HSTS headers

### Python HTTPS Server (Production)

```python
import ssl
import uvicorn
from pathlib import Path

def create_ssl_context() -> ssl.SSLContext:
    """Create secure SSL context for production."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Load certificate and private key
    context.load_cert_chain(
        certfile="/path/to/fullchain.pem",
        keyfile="/path/to/privkey.pem"
    )

    # Security settings
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_3

    # Strong cipher suites (Mozilla Intermediate compatibility)
    context.set_ciphers(
        'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS'
    )

    # Enable OCSP stapling
    context.options |= ssl.OP_NO_COMPRESSION
    context.options |= ssl.OP_SINGLE_ECDH_USE
    context.options |= ssl.OP_SINGLE_DH_USE

    return context

# Run FastAPI with TLS
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile="/path/to/privkey.pem",
        ssl_certfile="/path/to/fullchain.pem",
        ssl_version=ssl.PROTOCOL_TLS_SERVER,
        ssl_cert_reqs=ssl.CERT_NONE
    )
```

### FastAPI Security Headers

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Force HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# HSTS - Force HTTPS for 1 year
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Trust only specific hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

### Node.js HTTPS Server

```typescript
import https from 'https';
import fs from 'fs';
import express from 'express';

const app = express();

// SSL options
const sslOptions = {
  key: fs.readFileSync('/path/to/privkey.pem'),
  cert: fs.readFileSync('/path/to/fullchain.pem'),

  // Security settings
  minVersion: 'TLSv1.2' as const,
  maxVersion: 'TLSv1.3' as const,

  // Strong ciphers
  ciphers: [
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-CHACHA20-POLY1305'
  ].join(':'),

  // Prefer server cipher order
  honorCipherOrder: true
};

// Security headers middleware
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});

// Create HTTPS server
https.createServer(sslOptions, app).listen(443, () => {
  console.log('HTTPS Server running on port 443');
});
```

---

## Certificate Management

### Overview

X.509 certificates authenticate servers and enable TLS. Best practices:
- Use Let's Encrypt for automated certificate renewal
- Store private keys securely (never in version control)
- Monitor expiration dates
- Use Certificate Transparency

### Generate Self-Signed Certificate (Development Only)

```python
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

def generate_self_signed_cert(
    common_name: str = "localhost",
    days_valid: int = 365
) -> tuple[bytes, bytes]:
    """Generate self-signed certificate for development."""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    # Certificate subject and issuer
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Development"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    # Build certificate
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=days_valid))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(common_name),
                x509.DNSName(f"*.{common_name}"),
            ]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )

    # Serialize to PEM
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return cert_pem, key_pem

# Usage (development only!)
cert_pem, key_pem = generate_self_signed_cert("localhost")

with open("cert.pem", "wb") as f:
    f.write(cert_pem)

with open("key.pem", "wb") as f:
    f.write(key_pem)
```

### Certificate Verification

```python
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timezone

def verify_certificate(cert_pem: bytes) -> dict:
    """Verify certificate properties."""
    cert = x509.load_pem_x509_certificate(cert_pem)

    now = datetime.now(timezone.utc)

    return {
        'subject': cert.subject.rfc4514_string(),
        'issuer': cert.issuer.rfc4514_string(),
        'not_before': cert.not_valid_before_utc,
        'not_after': cert.not_valid_after_utc,
        'is_expired': now > cert.not_valid_after_utc,
        'days_until_expiry': (cert.not_valid_after_utc - now).days,
        'serial_number': cert.serial_number,
        'signature_algorithm': cert.signature_algorithm_oid._name
    }

# Usage
with open("cert.pem", "rb") as f:
    cert_info = verify_certificate(f.read())

if cert_info['is_expired']:
    print(f"Certificate expired on {cert_info['not_after']}")
elif cert_info['days_until_expiry'] < 30:
    print(f"Certificate expires in {cert_info['days_until_expiry']} days - renewal needed")
```

---

## Secrets Management

### Overview

Never hardcode secrets in source code. Use environment variables, secret managers, or encrypted configuration.

### Environment Variables Pattern

```python
import os
from functools import lru_cache
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    """Application settings with secrets."""

    # Database
    database_url: SecretStr

    # API Keys
    openai_api_key: SecretStr
    stripe_api_key: SecretStr

    # Encryption
    encryption_key: SecretStr
    jwt_secret: SecretStr

    # AWS
    aws_access_key_id: str
    aws_secret_access_key: SecretStr
    aws_region: str = "us-east-1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Cache settings singleton."""
    return Settings()

# Usage
settings = get_settings()

# Access secrets (get_secret_value() returns actual value)
db_url = settings.database_url.get_secret_value()

# Secrets are not logged
print(settings)  # Shows SecretStr('**********')
```

### AWS Secrets Manager Integration

```python
import boto3
import json
from functools import lru_cache

class SecretsManager:
    """AWS Secrets Manager integration."""

    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    @lru_cache(maxsize=128)
    def get_secret(self, secret_name: str) -> dict:
        """Retrieve and cache secret from AWS."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except Exception as e:
            raise ValueError(f"Failed to retrieve secret {secret_name}: {e}")

    def get_secret_value(self, secret_name: str, key: str) -> str:
        """Get specific key from secret."""
        secret = self.get_secret(secret_name)
        return secret.get(key)

# Usage
secrets = SecretsManager()

# Retrieve database credentials
db_creds = secrets.get_secret("prod/database")
db_url = f"postgresql://{db_creds['username']}:{db_creds['password']}@{db_creds['host']}/{db_creds['database']}"

# Retrieve API key
api_key = secrets.get_secret_value("prod/api-keys", "openai_key")
```

### HashiCorp Vault Integration

```python
import hvac
from functools import lru_cache

class VaultClient:
    """HashiCorp Vault integration."""

    def __init__(self, url: str, token: str):
        self.client = hvac.Client(url=url, token=token)

        if not self.client.is_authenticated():
            raise ValueError("Vault authentication failed")

    @lru_cache(maxsize=128)
    def get_secret(self, path: str) -> dict:
        """Read secret from Vault."""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response['data']['data']
        except Exception as e:
            raise ValueError(f"Failed to read secret {path}: {e}")

    def get_secret_value(self, path: str, key: str) -> str:
        """Get specific key from secret."""
        secret = self.get_secret(path)
        return secret.get(key)

# Usage
vault = VaultClient(
    url="https://vault.example.com:8200",
    token=os.getenv("VAULT_TOKEN")
)

# Read database password
db_password = vault.get_secret_value("secret/database", "password")

# Read encryption key
encryption_key = vault.get_secret_value("secret/encryption", "master_key")
```

---

## Envelope Encryption

### Overview

Envelope encryption is a multi-layer encryption pattern:
1. Generate Data Encryption Key (DEK) - encrypts data
2. Encrypt DEK with Key Encryption Key (KEK) - stored with data
3. KEK stored in secure key management system

This enables:
- Key rotation without re-encrypting all data
- Different DEKs for each record (data isolation)
- Integration with cloud KMS

### Envelope Encryption Pattern

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json
from base64 import b64encode, b64decode
from typing import Optional

class EnvelopeEncryption:
    """
    Envelope encryption pattern.

    Architecture:
    - Master Key (KEK) - stored in KMS
    - Data Keys (DEK) - unique per record, encrypted with KEK
    - Data - encrypted with DEK
    """

    def __init__(self, master_key: bytes):
        """Initialize with master key (KEK)."""
        self.kek = master_key
        self.kek_cipher = AESGCM(self.kek)

    def encrypt(self, plaintext: bytes, associated_data: Optional[bytes] = None) -> str:
        """
        Envelope encrypt data.

        Returns JSON with:
        - encrypted_dek: Data key encrypted with master key
        - encrypted_data: Data encrypted with data key
        - nonce: Nonce for data encryption
        - dek_nonce: Nonce for DEK encryption
        """
        # 1. Generate unique data encryption key
        dek = AESGCM.generate_key(bit_length=256)

        # 2. Encrypt data with DEK
        data_nonce = os.urandom(12)
        data_cipher = AESGCM(dek)
        encrypted_data = data_cipher.encrypt(data_nonce, plaintext, associated_data)

        # 3. Encrypt DEK with master key (KEK)
        dek_nonce = os.urandom(12)
        encrypted_dek = self.kek_cipher.encrypt(dek_nonce, dek, None)

        # 4. Return envelope (all components needed for decryption)
        envelope = {
            'encrypted_dek': b64encode(encrypted_dek).decode(),
            'dek_nonce': b64encode(dek_nonce).decode(),
            'encrypted_data': b64encode(encrypted_data).decode(),
            'data_nonce': b64encode(data_nonce).decode(),
            'aad': b64encode(associated_data).decode() if associated_data else None
        }

        return json.dumps(envelope)

    def decrypt(self, envelope: str) -> bytes:
        """
        Envelope decrypt data.

        Steps:
        1. Decrypt DEK using master key
        2. Decrypt data using DEK
        """
        data = json.loads(envelope)

        # 1. Decrypt data encryption key
        encrypted_dek = b64decode(data['encrypted_dek'])
        dek_nonce = b64decode(data['dek_nonce'])
        dek = self.kek_cipher.decrypt(dek_nonce, encrypted_dek, None)

        # 2. Decrypt data with DEK
        encrypted_data = b64decode(data['encrypted_data'])
        data_nonce = b64decode(data['data_nonce'])
        aad = b64decode(data['aad']) if data['aad'] else None

        data_cipher = AESGCM(dek)
        plaintext = data_cipher.decrypt(data_nonce, encrypted_data, aad)

        return plaintext

    def rotate_master_key(self, envelope: str, new_master_key: bytes) -> str:
        """
        Rotate master key without re-encrypting data.

        Only re-encrypts the DEK (fast operation).
        """
        data = json.loads(envelope)

        # 1. Decrypt DEK with old master key
        encrypted_dek = b64decode(data['encrypted_dek'])
        dek_nonce = b64decode(data['dek_nonce'])
        dek = self.kek_cipher.decrypt(dek_nonce, encrypted_dek, None)

        # 2. Re-encrypt DEK with new master key
        new_kek_cipher = AESGCM(new_master_key)
        new_dek_nonce = os.urandom(12)
        new_encrypted_dek = new_kek_cipher.encrypt(new_dek_nonce, dek, None)

        # 3. Update envelope (data unchanged!)
        data['encrypted_dek'] = b64encode(new_encrypted_dek).decode()
        data['dek_nonce'] = b64encode(new_dek_nonce).decode()

        return json.dumps(data)

# Usage
master_key = AESGCM.generate_key(bit_length=256)  # Store in KMS
envelope_cipher = EnvelopeEncryption(master_key)

# Encrypt user data
user_data = b"Sensitive PII data"
user_id = b"user_12345"
envelope = envelope_cipher.encrypt(user_data, associated_data=user_id)

# Store envelope in database (contains encrypted DEK + encrypted data)
db.save_encrypted_data(user_id, envelope)

# Later: Decrypt
decrypted = envelope_cipher.decrypt(envelope)

# Key rotation (fast - only re-encrypts DEK, not data!)
new_master_key = AESGCM.generate_key(bit_length=256)
rotated_envelope = envelope_cipher.rotate_master_key(envelope, new_master_key)
```

### AWS KMS Integration

```python
import boto3
import json
from base64 import b64encode, b64decode

class KMSEnvelopeEncryption:
    """Envelope encryption using AWS KMS."""

    def __init__(self, kms_key_id: str, region: str = "us-east-1"):
        self.kms_client = boto3.client('kms', region_name=region)
        self.kms_key_id = kms_key_id

    def encrypt(self, plaintext: bytes, context: dict = None) -> str:
        """Encrypt using KMS envelope encryption."""
        # 1. Generate data key from KMS
        response = self.kms_client.generate_data_key(
            KeyId=self.kms_key_id,
            KeySpec='AES_256',
            EncryptionContext=context or {}
        )

        # 2. Extract plaintext DEK and encrypted DEK
        dek = response['Plaintext']  # Use this to encrypt data
        encrypted_dek = response['CiphertextBlob']  # Store this

        # 3. Encrypt data with DEK
        cipher = AESGCM(dek)
        nonce = os.urandom(12)
        encrypted_data = cipher.encrypt(nonce, plaintext, None)

        # 4. Return envelope
        envelope = {
            'encrypted_dek': b64encode(encrypted_dek).decode(),
            'encrypted_data': b64encode(encrypted_data).decode(),
            'nonce': b64encode(nonce).decode()
        }

        return json.dumps(envelope)

    def decrypt(self, envelope: str, context: dict = None) -> bytes:
        """Decrypt using KMS envelope encryption."""
        data = json.loads(envelope)

        # 1. Decrypt DEK using KMS
        encrypted_dek = b64decode(data['encrypted_dek'])
        response = self.kms_client.decrypt(
            CiphertextBlob=encrypted_dek,
            EncryptionContext=context or {}
        )
        dek = response['Plaintext']

        # 2. Decrypt data with DEK
        cipher = AESGCM(dek)
        nonce = b64decode(data['nonce'])
        encrypted_data = b64decode(data['encrypted_data'])
        plaintext = cipher.decrypt(nonce, encrypted_data, None)

        return plaintext

# Usage
kms = KMSEnvelopeEncryption(kms_key_id="arn:aws:kms:us-east-1:123456789:key/abc-123")

# Encrypt with context (additional authentication)
context = {'user_id': '12345', 'data_type': 'pii'}
envelope = kms.encrypt(b"Sensitive data", context=context)

# Decrypt (must provide same context)
plaintext = kms.decrypt(envelope, context=context)
```

---

## Cryptographic Anti-Patterns

### Overview

Common cryptographic mistakes that lead to vulnerabilities.

### ❌ Anti-Pattern 1: MD5/SHA1 for Passwords

```python
# ❌ NEVER DO THIS
import hashlib

def bad_password_hash(password: str) -> str:
    """INSECURE: MD5 is broken, no salt, too fast."""
    return hashlib.md5(password.encode()).hexdigest()

def also_bad_password_hash(password: str) -> str:
    """INSECURE: SHA-1 is broken, no salt, too fast."""
    return hashlib.sha1(password.encode()).hexdigest()

# ✅ USE THIS INSTEAD
import bcrypt

def good_password_hash(password: str) -> str:
    """Secure: bcrypt with salt and work factor."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
```

### ❌ Anti-Pattern 2: ECB Mode

```python
# ❌ NEVER USE ECB MODE
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def bad_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """INSECURE: ECB mode reveals patterns in data."""
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()

# ✅ USE AUTHENTICATED ENCRYPTION
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def good_encrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Secure: AES-GCM with authentication."""
    cipher = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    return nonce, ciphertext
```

### ❌ Anti-Pattern 3: Predictable IVs

```python
# ❌ PREDICTABLE IV
def bad_iv_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """INSECURE: Static IV breaks security."""
    iv = b'\x00' * 16  # Static IV - NEVER DO THIS
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()

# ✅ RANDOM IV
def good_iv_encrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Secure: Random IV for each encryption."""
    iv = os.urandom(16)  # Unique IV every time
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, ciphertext
```

### ❌ Anti-Pattern 4: Unauthenticated Encryption

```python
# ❌ ENCRYPTION WITHOUT AUTHENTICATION
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def bad_encrypt_no_auth(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """INSECURE: No authentication - vulnerable to tampering."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, ciphertext  # Attacker can modify ciphertext

# ✅ AUTHENTICATED ENCRYPTION
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def good_encrypt_with_auth(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Secure: AES-GCM provides authentication."""
    cipher = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    return nonce, ciphertext  # Tampering detected automatically
```

### ❌ Anti-Pattern 5: Weak Random

```python
# ❌ PREDICTABLE RANDOMNESS
import random
import time

def bad_random_token() -> str:
    """INSECURE: Predictable random number generator."""
    random.seed(int(time.time()))  # Predictable seed
    return ''.join(random.choices('0123456789', k=32))

def bad_random_key() -> bytes:
    """INSECURE: Not cryptographically secure."""
    return bytes([random.randint(0, 255) for _ in range(32)])

# ✅ CRYPTOGRAPHICALLY SECURE RANDOM
import secrets

def good_random_token() -> str:
    """Secure: Cryptographically secure token."""
    return secrets.token_urlsafe(32)

def good_random_key() -> bytes:
    """Secure: Cryptographically secure key."""
    return secrets.token_bytes(32)
```

### ❌ Anti-Pattern 6: Key Derivation Without Salt

```python
# ❌ NO SALT
import hashlib

def bad_key_derivation(password: str) -> bytes:
    """INSECURE: No salt - vulnerable to rainbow tables."""
    return hashlib.sha256(password.encode()).digest()

# ✅ PROPER KDF WITH SALT
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os

def good_key_derivation(password: str) -> tuple[bytes, bytes]:
    """Secure: PBKDF2 with salt and iterations."""
    salt = os.urandom(32)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000
    )
    key = kdf.derive(password.encode())
    return key, salt
```

### ❌ Anti-Pattern 7: Timing Attacks

```python
# ❌ TIMING ATTACK VULNERABLE
def bad_token_compare(token1: str, token2: str) -> bool:
    """INSECURE: Early return leaks timing information."""
    if len(token1) != len(token2):
        return False

    for i in range(len(token1)):
        if token1[i] != token2[i]:
            return False  # Returns early - timing leak!

    return True

# ✅ CONSTANT-TIME COMPARISON
import hmac

def good_token_compare(token1: str, token2: str) -> bool:
    """Secure: Constant-time comparison."""
    return hmac.compare_digest(token1, token2)
```

### ❌ Anti-Pattern 8: Hardcoded Secrets

```python
# ❌ HARDCODED SECRETS
API_KEY = "sk_live_abc123xyz789"  # NEVER commit this!
ENCRYPTION_KEY = b"my_secret_key_12345"  # NEVER hardcode!
DATABASE_PASSWORD = "admin123"  # NEVER in source code!

# ✅ ENVIRONMENT VARIABLES
import os

API_KEY = os.getenv("API_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# ✅ SECRET MANAGER
from aws_secrets import SecretsManager

secrets = SecretsManager()
API_KEY = secrets.get_secret("prod/api_key")
```

### ❌ Anti-Pattern 9: Certificate Verification Disabled

```python
# ❌ DISABLE CERTIFICATE VERIFICATION
import requests

def bad_https_request():
    """INSECURE: Disables certificate verification."""
    response = requests.get(
        "https://api.example.com",
        verify=False  # NEVER DO THIS IN PRODUCTION
    )
    return response.json()

# ✅ PROPER CERTIFICATE VERIFICATION
import requests

def good_https_request():
    """Secure: Verify certificates."""
    response = requests.get(
        "https://api.example.com",
        verify=True,  # Default, but be explicit
        timeout=30
    )
    return response.json()
```

### ❌ Anti-Pattern 10: Rolling Your Own Crypto

```python
# ❌ CUSTOM ENCRYPTION ALGORITHM
def bad_custom_encrypt(plaintext: str, key: str) -> str:
    """INSECURE: Never implement your own crypto algorithm."""
    result = ""
    for i, char in enumerate(plaintext):
        # Some "clever" XOR-based encryption
        result += chr(ord(char) ^ ord(key[i % len(key)]))
    return result

# ✅ USE ESTABLISHED LIBRARIES
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def good_encrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Secure: Use established cryptographic libraries."""
    cipher = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    return nonce, ciphertext
```

---

## Best Practices Summary

### Password Hashing
- ✅ Use Argon2id, bcrypt, or scrypt
- ✅ Work factor: 250-500ms target time
- ✅ Unique salt per password (automatic in libraries)
- ❌ Never use MD5, SHA-1, or SHA-256 alone
- ❌ Never store plaintext passwords

### Encryption
- ✅ Use AES-256-GCM or ChaCha20-Poly1305
- ✅ Generate unique IV/nonce for each encryption
- ✅ Use authenticated encryption (AEAD modes)
- ❌ Never use ECB mode
- ❌ Never reuse nonces with the same key

### Key Management
- ✅ Generate keys with `secrets` or `os.urandom`
- ✅ Store keys in environment variables or secret managers
- ✅ Use envelope encryption for data encryption
- ✅ Rotate keys regularly
- ❌ Never hardcode keys in source code
- ❌ Never commit secrets to version control

### Random Generation
- ✅ Use `secrets` module for tokens/keys
- ✅ Use `os.urandom` for random bytes
- ❌ Never use `random` module for security
- ❌ Never use timestamps as randomness

### Comparisons
- ✅ Use `hmac.compare_digest` for secrets
- ✅ Use constant-time comparison for tokens
- ❌ Never use `==` for security-sensitive comparisons

### TLS/HTTPS
- ✅ Use TLS 1.2+ only
- ✅ Enable HSTS headers
- ✅ Verify certificates
- ❌ Never disable certificate verification
- ❌ Never use SSLv3 or TLS 1.0/1.1

### General
- ✅ Use well-tested cryptographic libraries
- ✅ Keep libraries up to date
- ✅ Follow defense in depth
- ❌ Never roll your own crypto algorithms
- ❌ Never trust user input without validation

---

## Security Checklist

Use this checklist for code review:

- [ ] Passwords hashed with bcrypt/Argon2id (not SHA-256)
- [ ] Work factor appropriate (250-500ms)
- [ ] Unique salt per password (automatic in libraries)
- [ ] AES-GCM or ChaCha20-Poly1305 for encryption
- [ ] Unique IV/nonce per encryption operation
- [ ] Keys generated with `secrets` or `os.urandom`
- [ ] No hardcoded secrets in source code
- [ ] Secrets loaded from environment/secret manager
- [ ] Constant-time comparison for tokens (`hmac.compare_digest`)
- [ ] TLS 1.2+ enforced
- [ ] Certificate verification enabled
- [ ] HSTS headers configured
- [ ] No use of deprecated algorithms (MD5, SHA-1, DES, 3DES, RC4)
- [ ] No custom crypto implementations
- [ ] All crypto libraries up to date

---

This skill provides production-ready cryptographic patterns. Always prioritize:
1. **Use established libraries** - Never implement your own crypto
2. **Defense in depth** - Multiple layers of security
3. **Principle of least privilege** - Minimize exposure of secrets
4. **Regular updates** - Keep cryptographic libraries current
5. **Security review** - Have crypto code reviewed by experts


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

