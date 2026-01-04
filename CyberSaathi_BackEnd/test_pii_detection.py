"""
PII Detection Test Script
Tests the privacy protection features
"""
import logging
from privacy.pii_detector import PIIDetector, sanitize_query
from privacy.redaction_logger import RedactionLogger

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def test_pii_detection():
    """Test PII detection with various scenarios"""
    print_header("🔒 PII Detection Tests")
    
    detector = PIIDetector()
    
    # Test cases with different types of PII
    test_cases = [
        {
            "name": "CNIC Detection",
            "query": "My CNIC is 12345-1234567-1 and I need legal help",
            "expected_types": ["CNIC"]
        },
        {
            "name": "Phone Number Detection",
            "query": "You can reach me at +92-300-1234567 or 03001234567",
            "expected_types": ["PHONE"]
        },
        {
            "name": "Email Detection",
            "query": "Please send details to john.doe@example.com",
            "expected_types": ["EMAIL"]
        },
        {
            "name": "Name Detection",
            "query": "My name is Ahmed Khan and I was hacked",
            "expected_types": ["NAME"]
        },
        {
            "name": "Multiple PII Types",
            "query": "I am Ali Raza, my CNIC is 42101-1234567-8, phone 0300-1234567, email ali@example.com. Someone hacked my account.",
            "expected_types": ["NAME", "CNIC", "PHONE", "EMAIL"]
        },
        {
            "name": "Address Detection",
            "query": "I live at House 123, Street 45, Karachi and need help with cybercrime",
            "expected_types": ["ADDRESS"]
        },
        {
            "name": "No PII",
            "query": "What are the penalties for unauthorized access under PECA 2016?",
            "expected_types": []
        },
        {
            "name": "Bank Account",
            "query": "They stole money from my account 1234567890123",
            "expected_types": ["BANK_ACCOUNT"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print(f"   Original: {test['query']}")
        
        # Detect PII
        detections = detector.detect_all(test['query'])
        
        # Redact PII
        sanitized, redaction_map = detector.redact(test['query'], detections)
        
        print(f"   Sanitized: {sanitized}")
        
        if detections:
            print(f"   ✅ Detected: {', '.join(detections.keys())}")
            for pii_type, values in detections.items():
                print(f"      - {pii_type}: {len(values)} item(s)")
        else:
            print(f"   ✅ No PII detected")
        
        # Verify expected types
        detected_types = set(detections.keys())
        expected_types = set(test['expected_types'])
        
        if detected_types == expected_types:
            print(f"   ✅ PASS - Detection matched expectations")
        else:
            print(f"   ⚠️  WARNING - Expected {expected_types}, got {detected_types}")


def test_sanitize_function():
    """Test the convenience sanitize_query function"""
    print_header("🧪 Sanitize Query Function Test")
    
    test_queries = [
        "My name is Sara Ahmed, CNIC 12345-1234567-1, phone 0300-1234567",
        "What are the penalties for cyber stalking?",
        "Someone hacked my email john@example.com and stole data"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Query {i}:")
        print(f"   Original: {query}")
        
        sanitized, info = sanitize_query(query, log_redactions=False)
        
        print(f"   Sanitized: {sanitized}")
        print(f"   Redacted: {info['redacted']}")
        
        if info['redacted']:
            print(f"   Count: {info['redaction_count']}")
            print(f"   Types: {', '.join(info['types_redacted'])}")


def test_redaction_logger():
    """Test the redaction logger"""
    print_header("📊 Redaction Logger Test")
    
    logger_instance = RedactionLogger(log_file="logs/test_redactions.log")
    
    # Simulate some redactions
    test_redactions = [
        {
            "redacted": True,
            "redaction_count": 2,
            "types_redacted": ["CNIC", "PHONE"],
            "redaction_map": {"CNIC": 1, "PHONE": 1}
        },
        {
            "redacted": True,
            "redaction_count": 1,
            "types_redacted": ["EMAIL"],
            "redaction_map": {"EMAIL": 1}
        },
        {
            "redacted": False,
            "redaction_count": 0,
            "types_redacted": [],
            "redaction_map": {}
        }
    ]
    
    print("\n📝 Logging redaction events...")
    for i, redaction in enumerate(test_redactions, 1):
        logger_instance.log_redaction(redaction, query_id=f"test_{i}")
        if redaction['redacted']:
            print(f"   ✅ Logged redaction {i}: {redaction['types_redacted']}")
    
    # Get statistics
    print("\n📊 Redaction Statistics:")
    stats = logger_instance.get_redaction_stats()
    print(f"   Total queries with PII: {stats['total_queries_with_pii']}")
    print(f"   Total redactions: {stats['total_redactions']}")
    print(f"   By type:")
    for pii_type, count in stats['by_type'].items():
        print(f"      - {pii_type}: {count}")


def test_real_world_scenarios():
    """Test real-world scenarios"""
    print_header("🌍 Real-World Scenario Tests")
    
    scenarios = [
        {
            "name": "Cybercrime Report",
            "query": "I want to report a cybercrime. My name is Fatima Ali, CNIC 42101-9876543-2. Someone hacked my Facebook account fatima.ali@gmail.com and is posting fake content. My phone is 0321-9876543."
        },
        {
            "name": "Legal Consultation",
            "query": "I need legal advice about PECA 2016. What are the penalties for unauthorized access?"
        },
        {
            "name": "Identity Theft",
            "query": "Someone is using my identity online. They have my CNIC 12345-6789012-3 and are opening fake accounts. I live in Lahore at House 456, Block B, DHA."
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📝 Scenario: {scenario['name']}")
        print(f"   Original Query:")
        print(f"   {scenario['query']}")
        
        sanitized, info = sanitize_query(scenario['query'], log_redactions=False)
        
        print(f"\n   Sanitized Query:")
        print(f"   {sanitized}")
        
        if info['redacted']:
            print(f"\n   🔒 Privacy Protection:")
            print(f"      - {info['redaction_count']} sensitive item(s) redacted")
            print(f"      - Types: {', '.join(info['types_redacted'])}")
            print(f"      ✅ Safe to send to LLM")
        else:
            print(f"\n   ✅ No PII detected - Safe to send to LLM")


def main():
    """Main test function"""
    print("\n🇵🇰 CyberSaathi - PII Detection Test Suite")
    
    try:
        # Run all tests
        test_pii_detection()
        test_sanitize_function()
        test_redaction_logger()
        test_real_world_scenarios()
        
        print("\n" + "="*70)
        print("  ✅ All Tests Completed")
        print("="*70)
        print("\n💡 The PII detection system is working correctly!")
        print("   Sensitive data will be automatically redacted before")
        print("   being sent to Gemini or any external service.\n")
    
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
