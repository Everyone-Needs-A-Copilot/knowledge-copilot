---
last_updated: 2026-02-25
status: active
name: data-protection
description: Data encryption, PII handling, privacy controls, and data lifecycle management. Use when implementing data security or reviewing data handling practices.
triggers:
  files: ["**/data/**", "**/encrypt/**", "**/privacy/**", "**/pii/**", "**/gdpr/**"]
  keywords: ["encryption", "PII", "data protection", "privacy", "GDPR", "CCPA", "personal data", "encrypt", "decrypt", "data classification", "data masking", "tokenization", "key management"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Data Protection Deep Expertise

This skill provides comprehensive guidance for protecting sensitive data throughout its lifecycle. Apply this knowledge when implementing encryption, handling PII, or ensuring privacy compliance.

## Data Classification

### Classification Levels

| Level | Description | Examples | Controls |
|-------|-------------|----------|----------|
| Public | No restrictions | Marketing, published docs | None required |
| Internal | Business use only | Meeting notes, plans | Access control |
| Confidential | Restricted access | Customer data, financials | Encryption + access control |
| Restricted | Highly sensitive | PII, credentials, trade secrets | Full protection suite |

### Classification Implementation

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

@dataclass
class DataField:
    name: str
    classification: DataClassification
    pii_type: Optional[str] = None
    encryption_required: bool = False
    masking_pattern: Optional[str] = None

# Define sensitive fields
SENSITIVE_FIELDS = {
    "email": DataField(
        name="email",
        classification=DataClassification.CONFIDENTIAL,
        pii_type="contact",
        encryption_required=True,
        masking_pattern=r"(.)[^@]*(@.*)"  # j***@example.com
    ),
    "ssn": DataField(
        name="ssn",
        classification=DataClassification.RESTRICTED,
        pii_type="government_id",
        encryption_required=True,
        masking_pattern=r"\d{3}-\d{2}-(\d{4})"  # ***-**-1234
    ),
    "credit_card": DataField(
        name="credit_card",
        classification=DataClassification.RESTRICTED,
        pii_type="financial",
        encryption_required=True,
        masking_pattern=r"\d{12}(\d{4})"  # ************1234
    ),
    "password": DataField(
        name="password",
        classification=DataClassification.RESTRICTED,
        encryption_required=True  # Actually hashed, not encrypted
    ),
}
```


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Encryption Patterns

### Encryption at Rest

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

class EncryptionService:
    """Field-level encryption for sensitive data"""

    def __init__(self, master_key: bytes = None):
        if master_key is None:
            master_key = os.environ.get("ENCRYPTION_KEY", "").encode()

        if not master_key:
            raise ValueError("ENCRYPTION_KEY environment variable required")

        # Derive key from master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"static_salt_for_derivation",  # Use proper salt in production
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key))
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext to base64-encoded ciphertext"""
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt base64-encoded ciphertext to plaintext"""
        return self.cipher.decrypt(ciphertext.encode()).decode()

encryption_service = EncryptionService()

# SQLAlchemy encrypted column type
from sqlalchemy import TypeDecorator, String

class EncryptedString(TypeDecorator):
    """Column type that encrypts/decrypts transparently"""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return encryption_service.encrypt(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return encryption_service.decrypt(value)
        return None

# Usage in model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)  # Not encrypted (searchable)
    ssn = Column(EncryptedString)  # Encrypted at rest
    credit_card = Column(EncryptedString)  # Encrypted at rest
```

### Encryption Key Management

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from datetime import datetime, timedelta
import hashlib

class KeyManager:
    """Manage encryption keys with rotation"""

    def __init__(self):
        self.keys = {}  # key_id -> key_data
        self.current_key_id = None

    def generate_key(self) -> str:
        """Generate new encryption key"""
        key_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        key = Fernet.generate_key()

        self.keys[key_id] = {
            "key": key,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=365),
            "status": "active"
        }

        self.current_key_id = key_id
        return key_id

    def get_key(self, key_id: str) -> bytes:
        """Get key by ID"""
        key_data = self.keys.get(key_id)
        if not key_data:
            raise ValueError(f"Key {key_id} not found")
        return key_data["key"]

    def rotate_keys(self):
        """Rotate to new key, keeping old keys for decryption"""
        # Mark current key as deprecated
        if self.current_key_id:
            self.keys[self.current_key_id]["status"] = "deprecated"

        # Generate new key
        new_key_id = self.generate_key()

        return new_key_id

    def encrypt_with_key_id(self, plaintext: str) -> tuple[str, str]:
        """Encrypt and return (ciphertext, key_id)"""
        key = self.get_key(self.current_key_id)
        cipher = Fernet(key)
        ciphertext = cipher.encrypt(plaintext.encode()).decode()
        return ciphertext, self.current_key_id

    def decrypt_with_key_id(self, ciphertext: str, key_id: str) -> str:
        """Decrypt using specific key ID"""
        key = self.get_key(key_id)
        cipher = Fernet(key)
        return cipher.decrypt(ciphertext.encode()).decode()

key_manager = KeyManager()
```

### Envelope Encryption

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class EnvelopeEncryption:
    """Envelope encryption for large data"""

    def __init__(self, master_key: bytes):
        self.master_key = master_key
        self.master_cipher = Fernet(master_key)

    def encrypt_large_data(self, data: bytes) -> dict:
        """Encrypt data using envelope encryption"""
        # Generate data encryption key (DEK)
        dek = Fernet.generate_key()

        # Encrypt data with DEK
        data_cipher = Fernet(dek)
        encrypted_data = data_cipher.encrypt(data)

        # Encrypt DEK with master key (KEK)
        encrypted_dek = self.master_cipher.encrypt(dek)

        return {
            "encrypted_data": encrypted_data,
            "encrypted_dek": encrypted_dek,
        }

    def decrypt_large_data(self, envelope: dict) -> bytes:
        """Decrypt envelope-encrypted data"""
        # Decrypt DEK with master key
        dek = self.master_cipher.decrypt(envelope["encrypted_dek"])

        # Decrypt data with DEK
        data_cipher = Fernet(dek)
        return data_cipher.decrypt(envelope["encrypted_data"])
```

## PII Handling

### PII Detection

```python
import re
from typing import List, Dict

class PIIDetector:
    """Detect PII in text and data"""

    PATTERNS = {
        "ssn": {
            "pattern": r"\b\d{3}-\d{2}-\d{4}\b",
            "type": "government_id",
            "severity": "critical"
        },
        "credit_card": {
            "pattern": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            "type": "financial",
            "severity": "critical"
        },
        "email": {
            "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "type": "contact",
            "severity": "high"
        },
        "phone": {
            "pattern": r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "type": "contact",
            "severity": "high"
        },
        "ip_address": {
            "pattern": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "type": "technical",
            "severity": "medium"
        },
    }

    def detect(self, text: str) -> List[Dict]:
        """Detect all PII in text"""
        findings = []

        for pii_type, config in self.PATTERNS.items():
            matches = re.finditer(config["pattern"], text)
            for match in matches:
                findings.append({
                    "type": pii_type,
                    "category": config["type"],
                    "severity": config["severity"],
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })

        return findings

    def contains_pii(self, text: str) -> bool:
        """Quick check if text contains any PII"""
        for config in self.PATTERNS.values():
            if re.search(config["pattern"], text):
                return True
        return False

pii_detector = PIIDetector()
```

### PII Masking/Redaction

```python
class PIIMasker:
    """Mask PII for safe display or logging"""

    MASK_PATTERNS = {
        "ssn": lambda m: f"***-**-{m[-4:]}",
        "credit_card": lambda m: f"{'*' * 12}{m[-4:]}",
        "email": lambda m: f"{m[0]}***@{m.split('@')[1]}",
        "phone": lambda m: f"***-***-{m[-4:]}",
    }

    def mask_value(self, value: str, pii_type: str) -> str:
        """Mask a single PII value"""
        masker = self.MASK_PATTERNS.get(pii_type)
        if masker:
            return masker(value)
        return "***REDACTED***"

    def mask_text(self, text: str) -> str:
        """Mask all PII in text"""
        detector = PIIDetector()
        findings = detector.detect(text)

        # Sort by position (reverse) to replace from end
        findings.sort(key=lambda f: f["start"], reverse=True)

        masked = text
        for finding in findings:
            masked_value = self.mask_value(finding["value"], finding["type"])
            masked = masked[:finding["start"]] + masked_value + masked[finding["end"]:]

        return masked

    def mask_dict(self, data: dict, sensitive_fields: set = None) -> dict:
        """Mask sensitive fields in dictionary"""
        if sensitive_fields is None:
            sensitive_fields = {"ssn", "credit_card", "password", "secret"}

        masked = {}
        for key, value in data.items():
            if key.lower() in sensitive_fields:
                masked[key] = "***REDACTED***"
            elif isinstance(value, str):
                masked[key] = self.mask_text(value)
            elif isinstance(value, dict):
                masked[key] = self.mask_dict(value, sensitive_fields)
            else:
                masked[key] = value

        return masked

pii_masker = PIIMasker()

# Safe logging middleware
import logging

class PIIFilter(logging.Filter):
    """Filter PII from log messages"""

    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = pii_masker.mask_text(record.msg)
        return True

# Apply to logger
logger = logging.getLogger("app")
logger.addFilter(PIIFilter())
```

### Data Tokenization

```python
import hashlib
import secrets
from typing import Optional

class TokenizationService:
    """Replace sensitive data with tokens"""

    def __init__(self):
        self.token_vault = {}  # token -> original value
        self.value_index = {}  # hash(value) -> token

    def tokenize(self, value: str) -> str:
        """Replace value with token"""
        value_hash = hashlib.sha256(value.encode()).hexdigest()

        # Return existing token if value already tokenized
        if value_hash in self.value_index:
            return self.value_index[value_hash]

        # Generate new token
        token = f"tok_{secrets.token_urlsafe(16)}"

        # Store mapping
        self.token_vault[token] = value
        self.value_index[value_hash] = token

        return token

    def detokenize(self, token: str) -> Optional[str]:
        """Retrieve original value from token"""
        return self.token_vault.get(token)

    def delete_token(self, token: str):
        """Delete token and original value"""
        if token in self.token_vault:
            value = self.token_vault[token]
            value_hash = hashlib.sha256(value.encode()).hexdigest()
            del self.token_vault[token]
            del self.value_index[value_hash]

tokenization_service = TokenizationService()
```

## Data Retention and Deletion

### Retention Policies

```python
from datetime import datetime, timedelta
from enum import Enum

class RetentionPolicy(str, Enum):
    IMMEDIATE = "immediate"      # Delete on request
    SHORT_TERM = "short_term"    # 30 days
    MEDIUM_TERM = "medium_term"  # 1 year
    LONG_TERM = "long_term"      # 7 years
    PERMANENT = "permanent"      # Never delete

RETENTION_PERIODS = {
    RetentionPolicy.IMMEDIATE: timedelta(days=0),
    RetentionPolicy.SHORT_TERM: timedelta(days=30),
    RetentionPolicy.MEDIUM_TERM: timedelta(days=365),
    RetentionPolicy.LONG_TERM: timedelta(days=365 * 7),
}

DATA_RETENTION_RULES = {
    "user_sessions": RetentionPolicy.SHORT_TERM,
    "audit_logs": RetentionPolicy.LONG_TERM,
    "user_profiles": RetentionPolicy.MEDIUM_TERM,
    "payment_records": RetentionPolicy.LONG_TERM,
    "marketing_preferences": RetentionPolicy.IMMEDIATE,
}

class RetentionManager:
    def get_deletion_date(self, data_type: str, created_at: datetime) -> datetime:
        """Calculate when data should be deleted"""
        policy = DATA_RETENTION_RULES.get(data_type, RetentionPolicy.MEDIUM_TERM)

        if policy == RetentionPolicy.PERMANENT:
            return None  # Never delete

        retention_period = RETENTION_PERIODS[policy]
        return created_at + retention_period

    async def cleanup_expired_data(self):
        """Delete data past retention period"""
        now = datetime.utcnow()

        for data_type, policy in DATA_RETENTION_RULES.items():
            if policy == RetentionPolicy.PERMANENT:
                continue

            retention_period = RETENTION_PERIODS[policy]
            cutoff = now - retention_period

            # Delete expired records
            await self._delete_expired(data_type, cutoff)

    async def _delete_expired(self, data_type: str, cutoff: datetime):
        """Delete records older than cutoff"""
        # Implementation depends on data store
        pass
```

### Secure Data Deletion

```python
import os

class SecureDeletion:
    """Securely delete sensitive data"""

    @staticmethod
    def secure_delete_file(filepath: str, passes: int = 3):
        """Overwrite file before deletion"""
        if not os.path.exists(filepath):
            return

        file_size = os.path.getsize(filepath)

        with open(filepath, "wb") as f:
            for _ in range(passes):
                # Overwrite with random data
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())

        # Delete file
        os.remove(filepath)

    @staticmethod
    def secure_clear_string(s: str) -> None:
        """Attempt to clear string from memory"""
        # Note: This is difficult in Python due to string immutability
        # Best practice: use bytes and clear after use
        pass

    @staticmethod
    def secure_delete_database_record(model, record_id: str):
        """Soft delete then schedule hard delete"""
        record = db.query(model).filter(model.id == record_id).first()
        if record:
            # Clear sensitive fields
            for field in SENSITIVE_FIELDS:
                if hasattr(record, field):
                    setattr(record, field, None)

            # Mark as deleted
            record.deleted_at = datetime.utcnow()
            db.commit()

            # Schedule hard delete after retention period
            schedule_hard_delete(model.__tablename__, record_id)
```

## Privacy Compliance

### GDPR Data Subject Rights

```python
class GDPRComplianceService:
    """Handle GDPR data subject rights"""

    async def handle_access_request(self, user_id: str) -> dict:
        """Right to Access - Export all user data"""
        user_data = {}

        # Collect from all data stores
        user_data["profile"] = await get_user_profile(user_id)
        user_data["orders"] = await get_user_orders(user_id)
        user_data["preferences"] = await get_user_preferences(user_id)
        user_data["activity_logs"] = await get_user_activity(user_id)

        # Include processing purposes
        user_data["processing_purposes"] = [
            "Account management",
            "Order fulfillment",
            "Service improvement"
        ]

        return user_data

    async def handle_deletion_request(self, user_id: str) -> dict:
        """Right to Erasure - Delete user data"""
        deletion_log = {}

        # Check for legal holds
        if await has_legal_hold(user_id):
            raise ValueError("Account under legal hold - cannot delete")

        # Delete from each system
        deletion_log["profile"] = await delete_user_profile(user_id)
        deletion_log["orders"] = await anonymize_orders(user_id)  # Keep for records
        deletion_log["preferences"] = await delete_preferences(user_id)

        return deletion_log

    async def handle_rectification_request(
        self,
        user_id: str,
        corrections: dict
    ) -> dict:
        """Right to Rectification - Correct inaccurate data"""
        # Validate corrections
        # Apply updates with audit trail
        return await update_user_data(user_id, corrections)

    async def handle_portability_request(self, user_id: str) -> bytes:
        """Right to Data Portability - Export in machine-readable format"""
        data = await self.handle_access_request(user_id)

        # Export as JSON
        return json.dumps(data, indent=2, default=str).encode()

    async def handle_restriction_request(self, user_id: str):
        """Right to Restriction - Limit processing"""
        user = await get_user(user_id)
        user.processing_restricted = True
        user.restriction_date = datetime.utcnow()
        await user.save()
```

### Consent Management

```python
class ConsentManager:
    """Manage user consent for data processing"""

    CONSENT_PURPOSES = [
        "essential",        # Required for service
        "analytics",        # Usage analytics
        "marketing",        # Marketing communications
        "third_party",      # Sharing with partners
        "personalization",  # Personalized experience
    ]

    async def record_consent(
        self,
        user_id: str,
        purpose: str,
        granted: bool,
        ip_address: str
    ):
        """Record consent decision with audit trail"""
        consent = Consent(
            user_id=user_id,
            purpose=purpose,
            granted=granted,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            source="user_action",
        )
        await consent.save()

    async def check_consent(self, user_id: str, purpose: str) -> bool:
        """Check if user has consented to purpose"""
        consent = await get_latest_consent(user_id, purpose)
        return consent and consent.granted

    async def withdraw_consent(self, user_id: str, purpose: str, ip_address: str):
        """Withdraw previously granted consent"""
        await self.record_consent(user_id, purpose, False, ip_address)

        # Trigger data processing stop
        await stop_processing_for_purpose(user_id, purpose)
```

## Security Controls

### Data Access Logging

```python
class DataAccessLogger:
    """Log all access to sensitive data"""

    async def log_access(
        self,
        user_id: str,
        data_type: str,
        data_id: str,
        action: str,
        ip_address: str,
        success: bool
    ):
        """Log data access event"""
        event = DataAccessEvent(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            data_type=data_type,
            data_id=data_id,
            action=action,  # read, write, delete
            ip_address=ip_address,
            success=success,
        )

        await event.save()

        # Alert on suspicious patterns
        await self._check_anomalies(user_id, data_type)

    async def _check_anomalies(self, user_id: str, data_type: str):
        """Detect unusual data access patterns"""
        recent_accesses = await get_recent_accesses(user_id, minutes=10)

        # Unusual volume
        if len(recent_accesses) > 100:
            await alert_security("High volume data access", user_id)

        # Unusual data types
        usual_types = await get_usual_data_types(user_id)
        if data_type not in usual_types:
            await alert_security("Unusual data type access", user_id)
```

## Anti-Patterns to Avoid

```python
# BAD: Storing sensitive data in plaintext
user.ssn = "123-45-6789"

# BAD: Logging sensitive data
logger.info(f"User {user.email} credit card: {user.credit_card}")

# BAD: Hardcoded encryption keys
ENCRYPTION_KEY = "my-secret-key-1234"

# BAD: Weak encryption
encrypted = base64.b64encode(data)  # Not encryption!

# BAD: No key rotation
# Using same key forever

# BAD: Returning unnecessary sensitive data
return {"user": user.__dict__}  # Includes all fields!
```

## Security Checklist

### Data Protection
- [ ] Data classified by sensitivity
- [ ] Encryption at rest for sensitive data
- [ ] Encryption in transit (TLS)
- [ ] Key management implemented
- [ ] Key rotation scheduled
- [ ] PII detection in place
- [ ] Data masking for logs/displays
- [ ] Retention policies defined
- [ ] Secure deletion implemented
- [ ] Access logging enabled
- [ ] GDPR/CCPA compliance verified

## Summary

Effective data protection requires:

1. **Classification**: Know your data sensitivity
2. **Encryption**: Protect data at rest and in transit
3. **Key management**: Secure keys, enable rotation
4. **Minimization**: Collect only what's needed
5. **Access control**: Limit who can access what
6. **Audit trails**: Log all sensitive data access
7. **Lifecycle management**: Retain and delete appropriately


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

