import logging
from typing import Optional, Dict, Any
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.x509.oid import NameOID
import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CertificateManager:
    def __init__(self):
        self.certificates = {}
        self.private_keys = {}
        
    def issue_certificate(self, 
                       common_name: str,
                       organization: str = "Quantum Network",
                       organizational_unit: str = "Security Division",
                       country: str = "US",
                       validity_days: int = 365) -> Optional[Dict[str, Any]]:
        """
        Issues a new X.509 certificate for a node.
        
        Args:
            common_name: Common name for the certificate
            organization: Organization name
            organizational_unit: Organizational unit
            country: Country code
            validity_days: Validity period in days
            
        Returns:
            Dict containing certificate data or None if failed
        """
        try:
            # Generate private key
            private_key = ec.generate_private_key(
                ec.SECP384R1()
            )
            
            # Create self-signed certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organizational_unit),
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
            ).add_extension(
                x509.BasicConstraints(ca=False, path_length=None),
                critical=True,
            ).add_extension(
                x509.KeyUsage(
                    key_cert_sign=False,
                    crl_sign=False,
                    digital_signature=True,
                    content_commitment=False,
                    key_encipherment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Store certificate and key
            cert_id = str(uuid.uuid4())
            self.certificates[cert_id] = cert
            self.private_keys[cert_id] = private_key
            
            # Return certificate information
            return {
                "id": cert_id,
                "certificate": cert,
                "private_key": private_key,
                "pem": cert.public_bytes(serialization.Encoding.PEM),
                "private_key_pem": private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            }
            
        except Exception as e:
            logger.error(f"Failed to issue certificate: {str(e)}")
            return None
    
    def validate_certificate(self, cert_pem: bytes) -> bool:
        """
        Validates an X.509 certificate.
        
        Args:
            cert_pem: PEM encoded certificate to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Load certificate
            cert = x509.load_pem_x509_certificate(cert_pem)
            
            # Check if certificate is expired
            if cert.not_valid_after < datetime.datetime.utcnow():
                logger.warning("Certificate is expired")
                return False
                
            # Check if certificate is not yet valid
            if cert.not_valid_before > datetime.datetime.utcnow():
                logger.warning("Certificate is not yet valid")
                return False
            
            # Additional validation can be added here
            # For example, checking certificate chain, CRL, OCSP, etc.
            
            return True
        except Exception as e:
            logger.error(f"Certificate validation failed: {str(e)}")
            return False

    def get_certificate(self, cert_id: str) -> Optional[x509.Certificate]:
        """
        Retrieve a certificate by ID.
        
        Args:
            cert_id: Certificate ID
            
        Returns:
            Certificate object or None
        """
        return self.certificates.get(cert_id)
        
    def get_private_key(self, cert_id: str) -> Optional[PrivateKeyTypes]:
        """
        Retrieve a private key by certificate ID.
        
        Args:
            cert_id: Certificate ID
            
        Returns:
            Private key or None
        """
        return self.private_keys.get(cert_id)
        
    def revoke_certificate(self, cert_id: str) -> bool:
        """
        Revoke a certificate.
        
        Args:
            cert_id: Certificate ID to revoke
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if cert_id in self.certificates:
                del self.certificates[cert_id]
            if cert_id in self.private_keys:
                del self.private_keys[cert_id]
            return True
        except Exception as e:
            logger.error(f"Failed to revoke certificate {cert_id}: {str(e)}")
            return False
            
    def list_certificates(self) -> Dict[str, str]:
        """
        List all certificate IDs and their common names.
        
        Returns:
            Dictionary of certificate IDs and common names
        """
        result = {}
        for cert_id, cert in self.certificates.items():
            try:
                common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                result[cert_id] = common_name
            except:
                result[cert_id] = "Unknown"
        return result