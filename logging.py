from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import time
import json
from enum import Enum

@dataclass
class LogLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"

@dataclass
class LogEntry:
    """Entry in the logging system"""
    id: str
    level: LogLevel = LogLevel.INFO
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    category: str = ""
    
    @classmethod
def create_error(cls, message: str, category: str = "error"):
        return cls(
            level=LogLevel.ERROR,
            message=message,
            category=category
        )

    @classmethod
def create_warning(cls, message: str, category: str = "warning"):
        return cls(
            level=LogLevel.WARNING,
            message=message,
            category=category
        )

    @classmethod
def create_info(cls, message: str, category: str = "info"):
        return cls(
            level=LogLevel.INFO,
            message=message,
            category=category
        )

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)

@dataclass
class Logger:
    """Central logging system"""
    
    name: str
    log_level: LogLevel = LogLevel.INFO
    
    def log(self, level: LogLevel, message: str, category: str = ""):
        if level < self.log_level:
            return
        
        entry = LogEntry(
            id=str(uuid.uuid4()),
            level=level,
            message=message,
            category=category
        )
        
        self._log_entry(entry)
        
    def error(self, message: str, category: str = "error"):
        self.log(LogLevel.ERROR, message, category)

    def warning(self, message: str, category: str = "warning"):
        self.log(LogLevel.WARNING, message, category)

    def info(self, message: str, category: str = "info"):
        self.log(LogLevel.INFO, message, category)

    def debug(self, message: str, category: str = "debug"):
        self.log(LogLevel.DEBUG, message, category)

    def _log_entry(self, entry: LogEntry):
        # Implementation for logging entry
        pass