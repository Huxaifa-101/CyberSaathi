"""
Redaction Logger
Logs PII redactions for audit and monitoring (without storing actual PII)
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


class RedactionLogger:
    """
    Logs PII redaction events for audit purposes
    Does NOT store actual PII values, only metadata
    """
    
    def __init__(self, log_file: str = None):
        """
        Initialize redaction logger
        
        Args:
            log_file: Path to log file (optional)
        """
        if log_file:
            self.log_file = Path(log_file)
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            self.log_file = None
    
    def log_redaction(self, redaction_info: Dict, query_id: str = None):
        """
        Log a redaction event
        
        Args:
            redaction_info: Information about what was redacted
            query_id: Optional query identifier
        """
        if not redaction_info.get("redacted"):
            return  # Nothing to log
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_id": query_id,
            "redaction_count": redaction_info.get("redaction_count", 0),
            "types_redacted": redaction_info.get("types_redacted", []),
            "redaction_map": redaction_info.get("redaction_map", {})
        }
        
        # Log to file if configured
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + '\n')
            except Exception as e:
                logger.error(f"Failed to write redaction log: {e}")
        
        # Also log to standard logger
        logger.info(
            f"PII Redaction Event - "
            f"Types: {', '.join(log_entry['types_redacted'])}, "
            f"Count: {log_entry['redaction_count']}"
        )
    
    def get_redaction_stats(self) -> Dict:
        """
        Get statistics about redactions
        
        Returns:
            Dictionary with redaction statistics
        """
        if not self.log_file or not self.log_file.exists():
            return {
                "total_redactions": 0,
                "by_type": {},
                "total_queries_with_pii": 0
            }
        
        stats = {
            "total_redactions": 0,
            "by_type": {},
            "total_queries_with_pii": 0
        }
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        stats["total_queries_with_pii"] += 1
                        stats["total_redactions"] += entry.get("redaction_count", 0)
                        
                        for pii_type, count in entry.get("redaction_map", {}).items():
                            if pii_type not in stats["by_type"]:
                                stats["by_type"][pii_type] = 0
                            stats["by_type"][pii_type] += count
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.error(f"Failed to read redaction stats: {e}")
        
        return stats
