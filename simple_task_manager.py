import json
import os
from datetime import datetime

class Task:
    """
    Represents a task with title, priority, and completion status.
    """

    def __init__(self, title, priority, due_date=None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.id = hash((title + str(datetime.now())).encode())

    def to_dict(self):
        """
        Convert task to dictionary for JSON storage.
        """
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @staticmethod
def from_dict(data):
        """
        Create task from dictionary.
        """
        task = Task(data['title'], data['priority'], data.get('due_date'))
        task.id = data['id']
        task.completed = data['completed']
        return task
class TaskManager:
    """
    Manages task creation, completion, and retrieval.
    """

    def __init__(self, storage_file='tasks.json'):
        self.storage_file = storage_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """
        Load tasks from storage file.
        """
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return [Task.from_dict(task) for task in json.load(f)]
        return []

    def _save_tasks(self):
        """
        Save tasks to storage file.
        """
        with open(self.storage_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def create_task(self, title, priority, due_date=None):
        """
        Create a new task.
        """
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        self._save_tasks()
        return task

    def complete_task(self, task_id):
        """
        Mark task as completed.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self._save_tasks()
                return task
        return None

    def get_tasks(self):
        """
        Get all tasks.
        """
        return self.tasks

    def get_active_tasks(self):
        """
        Get active (incomplete) tasks.
        """
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self):
        """
        Get completed tasks.
        """
        return [task for task in self.tasks if task.completed]

    def delete_task(self, task_id):
        """
        Delete a task by ID.
        """
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self._save_tasks()
                return True
        return False