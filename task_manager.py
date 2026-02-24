import json
import os
from datetime import datetime

class Task:
    """
    Represents a single task with various properties.
    """

    def __init__(self, title, priority, due_date=None, project=None, context=None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.project = project
        self.context = context
        self.id = hash((self.title + str(datetime.now())).encode())
        self.completed = False
        self.created_at = datetime.now()

    def to_dict(self):
        """
        Convert task to dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'project': self.project,
            'context': self.context,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
def from_dict(data):
        """
        Create task from dictionary.
        """
        due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        task = Task(
            title=data['title'],
            priority=data['priority'],
            due_date=due_date,
            project=data.get('project'),
            context=data.get('context')
        )
        task.id = data['id']
        task.completed = data['completed']
        task.created_at = datetime.fromisoformat(data['created_at'])
        return task

class TaskManager:
    """
    Manages task operations including creation, completion, and deletion.
    """

    def __init__(self, storage_file='tasks.json'):
        self.storage_file = storage_file
        self.tasks = self._load_tasks()
        self.next_id = len(self.tasks) + 1

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

    def create_task(self, title, priority, due_date=None, project=None, context=None):
        """
        Create a new task.

        Args:
            title (str): Task title
            priority (int): Priority level (1-5)
            due_date (str, optional): Due date in YYYY-MM-DD format
            project (str, optional): Project name
            context (str, optional): Context information

        Returns:
            Task: Created task

        Raises:
            ValueError: If title is empty or priority is invalid
        """
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if priority < 1 or priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        
        task = Task(
            title=title.strip(),
            priority=priority,
            due_date=due_date,
            project=project,
            context=context
        )
        
        self.tasks.append(task)
        self._save_tasks()
        
        return task

    def complete_task(self, task_id):
        """
        Mark task as completed.

        Args:
            task_id (int): Task ID

        Returns:
            Task: Completed task or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self._save_tasks()
                return task
        return None

    def delete_task(self, task_id):
        """
        Delete task permanently.

        Args:
            task_id (int): Task ID

        Returns:
            bool: True if task was deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self._save_tasks()
                return True
        return False

    def get_tasks(self, status='all'):
        """
        Get tasks filtered by status.

        Args:
            status (str): 'all', 'active', or 'completed'

        Returns:
            list: Filtered tasks
        """
        if status == 'all':
            return self.tasks
        elif status == 'active':
            return [t for t in self.tasks if not t.completed]
        elif status == 'completed':
            return [t for t in self.tasks if t.completed]
        return []

    def get_overdue_tasks(self):
        """
        Get all overdue tasks.

        Returns:
            list: Overdue tasks
        """
        overdue = []
        now = datetime.now().date()
        
        for task in self.tasks:
            if task.due_date:
                try:
                    due_date = task.due_date.date()
                    if due_date < now and not task.completed:
                        overdue.append(task)
                except Exception:
                    continue
        
        return overdue

    def update_task(self, task_id, **kwargs):
        """
        Update task properties.

        Args:
            task_id (int): Task ID
            **kwargs: Task properties to update

        Returns:
            Task: Updated task or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self._save_tasks()
                return task
        return None

    def get_task_by_id(self, task_id):
        """
        Retrieve task by ID.

        Args:
            task_id (int): Task ID

        Returns:
            Task: Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def __str__(self):
        """
        String representation of task manager.
        """
        return json.dumps([task.to_dict() for task in self.tasks], indent=4)

    def generate_stats(self):
        """
        Generate task statistics.

        Returns:
            dict: Task statistics
        """
        return {
            'total_tasks': len(self.tasks),
            'active_tasks': len([t for t in self.tasks if not t.completed]),
            'completed_tasks': len([t for t in self.tasks if t.completed]),
            'overdue_tasks': len(self.get_overdue_tasks()),
        }

if __name__ == '__main__':
    manager = TaskManager()
    
    # Create tasks
    task1 = manager.create_task("Write report", 5, due_date="2026-11-20")
    task2 = manager.create_task("Review code", 4, due_date="2026-11-18")
    task3 = manager.create_task("Team meeting", 3, due_date="2026-11-22")
    
    # Complete task
    manager.complete_task(task1.id)
    
    # Update task
    manager.update_task(task2.id, title="Review pull request", priority=3)
    
    # Get tasks
    print("Active tasks:")
    for task in manager.get_tasks('active'):
        print(task.title)
    
    print("\nStats:")
    print(manager.generate_stats())