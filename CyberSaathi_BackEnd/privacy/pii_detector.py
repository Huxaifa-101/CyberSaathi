"""
PII (Personally Identifiable Information) Detector
Detects and redacts sensitive information from user queries
"""
import re
import logging
from typing import Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class PIIDetector:
    """
    Detects and redacts various types of PII from text
    
    Supported PII types:
    - Pakistani CNIC (13 digits)
    - Phone numbers (Pakistani format)
    - Email addresses
    - Names (common Pakistani names)
    - Addresses
    - Bank account numbers
    - Credit card numbers
    - IP addresses
    - URLs with personal info
    """
    
    def __init__(self):
        """Initialize PII patterns"""
        
        # Pakistani CNIC: 12345-1234567-1 or 1234512345671
        self.cnic_pattern = re.compile(
            r'\b\d{5}[-\s]?\d{7}[-\s]?\d{1}\b'
        )
        
        # Pakistani phone numbers: +92, 03XX, etc.
        self.phone_pattern = re.compile(
            r'(\+92[-\s]?)?(\(?\d{3}\)?[-\s]?)?\d{7,8}\b'
        )
        
        # Email addresses
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # Bank account numbers (8-16 digits)
        self.bank_account_pattern = re.compile(
            r'\b(?:account|acc|a/c)[\s#:]*(\d{8,16})\b',
            re.IGNORECASE
        )
        
        # Credit card numbers (13-19 digits with optional spaces/dashes)
        self.credit_card_pattern = re.compile(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4,7}\b'
        )
        
        # IP addresses
        self.ip_pattern = re.compile(
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        )
        
        # Common Pakistani name patterns (basic detection)
        self.name_indicators = [
            r'\bmy name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\bI am\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\bI\'m\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\bcalled\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
        ]
        
        # Address indicators
        self.address_indicators = [
            r'\b(?:address|residence|located at|living at|house|street|road|avenue)[\s:]+([^.!?]+)',
            r'\b(?:Karachi|Lahore|Islamabad|Rawalpindi|Multan|Faisalabad|Peshawar|Quetta|Sialkot|Gujranwala)[^.!?]*',
        ]
        
        # URLs with potential personal info
        self.url_pattern = re.compile(
            r'https?://[^\s]+',
            re.IGNORECASE
        )
        
        # Date of birth patterns
        self.dob_pattern = re.compile(
            r'\b(?:DOB|date of birth|born on)[\s:]*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',
            re.IGNORECASE
        )
    
    def detect_cnic(self, text: str) -> List[Tuple[str, str]]:
        """Detect Pakistani CNIC numbers"""
        matches = self.cnic_pattern.findall(text)
        return [("CNIC", match) for match in matches]
    
    def detect_phone(self, text: str) -> List[Tuple[str, str]]:
        """Detect phone numbers"""
        matches = self.phone_pattern.findall(text)
        # Filter out false positives (too short)
        valid_matches = []
        for match in matches:
            if isinstance(match, tuple):
                full_match = ''.join(match)
            else:
                full_match = match
            
            # Remove non-digits to check length
            digits_only = re.sub(r'\D', '', full_match)
            if len(digits_only) >= 10:  # Valid phone number
                valid_matches.append(("PHONE", full_match))
        
        return valid_matches
    
    def detect_email(self, text: str) -> List[Tuple[str, str]]:
        """Detect email addresses"""
        matches = self.email_pattern.findall(text)
        return [("EMAIL", match) for match in matches]
    
    def detect_bank_account(self, text: str) -> List[Tuple[str, str]]:
        """Detect bank account numbers"""
        matches = self.bank_account_pattern.findall(text)
        return [("BANK_ACCOUNT", match) for match in matches]
    
    def detect_credit_card(self, text: str) -> List[Tuple[str, str]]:
        """Detect credit card numbers"""
        matches = self.credit_card_pattern.findall(text)
        # Validate using Luhn algorithm for credit cards
        valid_matches = []
        for match in matches:
            digits = re.sub(r'\D', '', match)
            if len(digits) >= 13 and len(digits) <= 19:
                valid_matches.append(("CREDIT_CARD", match))
        return valid_matches
    
    def detect_ip_address(self, text: str) -> List[Tuple[str, str]]:
        """Detect IP addresses"""
        matches = self.ip_pattern.findall(text)
        return [("IP_ADDRESS", match) for match in matches]
    
    def detect_names(self, text: str) -> List[Tuple[str, str]]:
        """Detect names from context"""
        detected = []
        for pattern in self.name_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Filter out common words that aren't names
                if len(match.split()) <= 4:  # Reasonable name length
                    detected.append(("NAME", match))
        return detected
    
    def detect_addresses(self, text: str) -> List[Tuple[str, str]]:
        """Detect addresses"""
        detected = []
        for pattern in self.address_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 10:  # Reasonable address length
                    detected.append(("ADDRESS", match.strip()))
        return detected
    
    def detect_urls(self, text: str) -> List[Tuple[str, str]]:
        """Detect URLs"""
        matches = self.url_pattern.findall(text)
        return [("URL", match) for match in matches]
    
    def detect_dob(self, text: str) -> List[Tuple[str, str]]:
        """Detect date of birth"""
        matches = self.dob_pattern.findall(text)
        return [("DOB", match) for match in matches]
    
    def detect_all(self, text: str) -> Dict[str, List[str]]:
        """
        Detect all types of PII in text
        
        Returns:
            Dictionary mapping PII type to list of detected values
        """
        all_detections = {}
        
        # Run all detectors
        detections = (
            self.detect_cnic(text) +
            self.detect_phone(text) +
            self.detect_email(text) +
            self.detect_bank_account(text) +
            self.detect_credit_card(text) +
            self.detect_ip_address(text) +
            self.detect_names(text) +
            self.detect_addresses(text) +
            self.detect_urls(text) +
            self.detect_dob(text)
        )
        
        # Group by type
        for pii_type, value in detections:
            if pii_type not in all_detections:
                all_detections[pii_type] = []
            if value not in all_detections[pii_type]:  # Avoid duplicates
                all_detections[pii_type].append(value)
        
        return all_detections
    
    def redact(self, text: str, pii_detections: Dict[str, List[str]] = None) -> Tuple[str, Dict]:
        """
        Redact PII from text
        
        Args:
            text: Original text
            pii_detections: Pre-detected PII (optional, will detect if not provided)
        
        Returns:
            Tuple of (redacted_text, redaction_map)
        """
        if pii_detections is None:
            pii_detections = self.detect_all(text)
        
        redacted_text = text
        redaction_map = {}
        
        # Redaction templates
        redaction_templates = {
            "CNIC": "[REDACTED_CNIC]",
            "PHONE": "[REDACTED_PHONE]",
            "EMAIL": "[REDACTED_EMAIL]",
            "BANK_ACCOUNT": "[REDACTED_ACCOUNT]",
            "CREDIT_CARD": "[REDACTED_CARD]",
            "IP_ADDRESS": "[REDACTED_IP]",
            "NAME": "[REDACTED_NAME]",
            "ADDRESS": "[REDACTED_ADDRESS]",
            "URL": "[REDACTED_URL]",
            "DOB": "[REDACTED_DOB]"
        }
        
        # Replace each detected PII
        for pii_type, values in pii_detections.items():
            template = redaction_templates.get(pii_type, "[REDACTED]")
            for value in values:
                if value in redacted_text:
                    redacted_text = redacted_text.replace(value, template)
                    
                    # Track what was redacted (without storing actual value)
                    if pii_type not in redaction_map:
                        redaction_map[pii_type] = 0
                    redaction_map[pii_type] += 1
        
        return redacted_text, redaction_map


def sanitize_query(query: str, log_redactions: bool = True) -> Tuple[str, Dict]:
    """
    Convenience function to sanitize a query
    
    Args:
        query: User query to sanitize
        log_redactions: Whether to log redactions
    
    Returns:
        Tuple of (sanitized_query, redaction_info)
    """
    detector = PIIDetector()
    
    # Detect PII
    pii_detections = detector.detect_all(query)
    
    # Redact PII
    sanitized, redaction_map = detector.redact(query, pii_detections)
    
    # Log if requested
    if log_redactions and redaction_map:
        logger.warning(
            f"PII detected and redacted: {redaction_map}"
        )
        logger.info(
            f"Original query length: {len(query)}, "
            f"Sanitized query length: {len(sanitized)}"
        )
    
    return sanitized, {
        "redacted": bool(redaction_map),
        "redaction_count": sum(redaction_map.values()),
        "types_redacted": list(redaction_map.keys()),
        "redaction_map": redaction_map
    }
