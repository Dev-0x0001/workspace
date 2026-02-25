from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(kw_only=True)
class MemoryEntry:
    """Represents an entry in memory"""

    id: str = field(default_factory=lambda: str(uuid4()))
    content: str
    priority: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return self.__dict__.copy()


dataclass(kw_only=True)
class ShortTermMemory:
    """Short-term memory with limited capacity"""

    max_entries: int = 10
    entries: List[MemoryEntry] = field(default_factory=list)

    def add(self, content: str, priority: int = 1):
        """Add a new memory entry"""
        entry = MemoryEntry(content=content, priority=priority)
        
        if len(self.entries) >= self.max_entries:
            # Remove lowest priority entry if full
            self.entries.sort(key=lambda x: x.priority)
            self.entries.pop(0)
        
        self.entries.append(entry)
        self.entries.sort(key=lambda x: x.priority, reverse=True)
        
        return entry

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all memory entries"""
        return [entry.to_dict() for entry in self.entries]

    def clear(self):
        """Clear all memory entries"""
        self.entries.clear()


dataclass(kw_only=True)
class LongTermMemory:
    """Long-term memory with indexing and search"""

    entries: List[MemoryEntry] = field(default_factory=list)

    def add(self, content: str, priority: int = 1):
        """Add a new memory entry"""
        entry = MemoryEntry(content=content, priority=priority)
        self.entries.append(entry)
        return entry

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search memory for entries containing query"""
        return [entry.to_dict() for entry in self.entries if query.lower() in entry.content.lower()]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all memory entries"""
        return [entry.to_dict() for entry in self.entries]


dataclass(kw_only=True)
class MemoryManager:
    """Manages both short-term and long-term memory"""

    short_term: ShortTermMemory = field(default_factory=ShortTermMemory)
    long_term: LongTermMemory = field(default_factory=LongTermMemory)

    def add_memory(self, content: str, priority: int = 1):
        """Add a new memory (short-term by default, also long-term)
        
        Args:
            content: The memory content
            priority: Memory priority (1-5, higher = more important)
        """
        if priority < 1 or priority > 5:
            priority = 1
        
        self.short_term.add(content, priority=priority)
        self.long_term.add(content, priority=priority)

    def get_memories(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories (short-term first)
        
        Args:
            count: Number of memories to return
        """
        memories = []
        
        # Add short-term memories first
        for entry in self.short_term.entries[:count]:
            memories.append(entry.to_dict())
            count -= 1
            if count == 0:
                break
        
        # Add long-term memories if more needed
        if count > 0:
            for entry in self.long_term.entries[:count]:
                memories.append(entry.to_dict())
                count -= 1
                if count == 0:
                    break
        
        return memories