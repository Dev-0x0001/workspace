from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class FeedbackRecord:
    """Data class representing a feedback record"""
    id: str
    user_id: str
    feedback_type: str
    content: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
def from_dict(cls, data: Dict[str, Any]) -> "FeedbackRecord":
        """Factory method to create from dictionary"""
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.__dict__

class FeedbackDatabase:
    """A robust feedback database with CRUD operations"""

    def __init__(self):
        self.records: Dict[str, FeedbackRecord] = {}
        self.next_id: int = 1
        self._validate_schema()

    def _validate_schema(self) -> bool:
        """Validate database schema (for migration purposes)"""
        # This is a simple example - could be more complex
        required_fields = {'id', 'user_id', 'feedback_type', 'content', 'timestamp'}
        test_record = FeedbackRecord(
            id="test", user_id="user1", feedback_type="suggestion",
            content="Test feedback", timestamp="2023-01-01"
        )
        # Check if all required fields exist
        return required_fields.issubset(test_record.__dict__.keys())

    def create(self, user_id: str, feedback_type: str, content: str, 
               timestamp: Optional[str] = None) -> FeedbackRecord:
        """Create a new feedback record"""
        
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # Generate unique ID
        record_id = str(self.next_id)
        self.next_id += 1
        
        record = FeedbackRecord(
            id=record_id,
            user_id=user_id,
            feedback_type=feedback_type,
            content=content,
            timestamp=timestamp
        )
        
        self.records[record_id] = record
        return record

    def retrieve(self, record_id: str) -> Optional[FeedbackRecord]:
        """Retrieve a feedback record by ID"""
        return self.records.get(record_id)

    def update(self, record_id: str, updates: Dict[str, Any]) -> 
               Optional[FeedbackRecord]:
        """Update a feedback record"""
        record = self.retrieve(record_id)
        if record:
            # Apply updates
            for key, value in updates.items():
                setattr(record, key, value)
            
            self.records[record_id] = record
            return record
        return None

    def list_all(self) -> List[FeedbackRecord]:
        """List all feedback records"""
        return list(self.records.values())

    def delete(self, record_id: str) -> bool:
        """Delete a feedback record"""
        if record_id in self.records:
            del self.records[record_id]
            return True
        return False

    def list_by_type(self, feedback_type: str) -> List[FeedbackRecord]:
        """List records by feedback type"""
        return [r for r in self.records.values() if r.feedback_type == feedback_type]

    def list_by_user(self, user_id: str) -> List[FeedbackRecord]:
        """List records by user ID"""
        return [r for r in self.records.values() if r.user_id == user_id]

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            'total_records': len(self.records),
            'record_ids': list(self.records.keys()),
            'types_distribution': {
                t: len(list_by_type(t)) for t in set(r.feedback_type 
                    for r in self.records.values())
            }
        }

    def backup(self) -> Dict[str, Any]:
        """Create a backup of the database"""
        return {
            'schema_version': 1,
            'records': [r.to_dict() for r in self.records.values()]
        }

    def restore_from_backup(self, backup: Dict[str, Any]) -> None:
        """Restore database from backup"""
        if backup.get('schema_version') == 1:
            self.records = {r['id']: FeedbackRecord.from_dict(r) 
                               for r in backup['records']}
            self.next_id = int(max((int(r['id']) for r in backup['records']), 
                                    default=0)) + 1
        else:
            raise ValueError("Backup schema version mismatch")