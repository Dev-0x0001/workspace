import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class TodoList:
    """
    A comprehensive todo list manager that supports:
    - Task creation with priorities and deadlines
    - Categorization by project, context, and urgency
    - Smart prioritization (Eisenhower Matrix)
    - Due date tracking
    - Recurring tasks
    """

    def __init__(self, storage_path: str = "todo.json") -> None:
        """
        Initialize the todo list manager.
        Args:
            storage_path: Path to storage file
        """
        self.storage_path = storage_path
        self.tasks: Dict[str, Dict] = {}
        self.completed_tasks: Dict[str, Dict] = {}
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self) -> None:
        """
        Load tasks from storage file.
        """
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data = json.load(f)
            self.tasks = data.get("tasks", {})
            self.completed_tasks = data.get("completed_tasks", {})
            if "next_id" in data:
                self.next_id = data["next_id"]
        else:
            self.tasks = {}
            self.completed_tasks = {}

    def save_tasks(self) -> None:
        """
        Save tasks to storage file.
        """
        with open(self.storage_path, "w") as f:
            json.dump({
                "tasks": self.tasks,
                "completed_tasks": self.completed_tasks,
                "next_id": self.next_id,
            }, f, indent=4)

    def create_task(self, description: str, priority: int = 3, 
                    due_date: Optional[str] = None, 
                    project: Optional[str] = None, 
                    context: Optional[str] = None, 
                    recurring: Optional[str] = None) -> Dict:
        """
        Create a new task.
        Args:
            description: Task description
            priority: Priority level (1-5, default: 3)
            due_date: Due date (YYYY-MM-DD)
            project: Project name
            context: Context (location/people)
            recurring: Recurrence pattern ('daily', 'weekly', 'monthly', 
                      or 'every-X-days')
        Returns:
            Created task
        """
        if description.strip() == "":
            raise ValueError("Task description cannot be empty")

        task_id = str(self.next_id)
        self.next_id += 1

        # Validate priority
        if priority < 1 or priority > 5:
            raise ValueError("Priority must be between 1 and 5")

        # Parse due date
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                if parsed_due_date < datetime.now().date():
                    raise ValueError("Due date cannot be in past")
            except ValueError:
                raise ValueError("Invalid due date format. Use YYYY-MM-DD")

        # Create task
        task = {
            "id": task_id,
            "description": description.strip(),
            "priority": priority,
            "due_date": parsed_due_date.isoformat() if parsed_due_date else None,
            "project": project,
            "context": context,
            "recurring": recurring,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None,
        }

        self.tasks[task_id] = task
        self.save_tasks()
        return task

    def complete_task(self, task_id: str) -> Optional[Dict]:
        """
        Mark a task as completed.
        Args:
            task_id: Task ID
        Returns:
            The completed task or None if not found
        """
        task = self.find_task(task_id)
        if not task:
            return None

        if task_id in self.completed_tasks:
            # If already completed, update completion time
            task["completed_at"] = datetime.now().isoformat()
            self.completed_tasks[task_id] = task
        else:
            # Move from tasks to completed_tasks
            task["completed_at"] = datetime.now().isoformat()
            self.completed_tasks[task_id] = task
            del self.tasks[task_id]

        self.save_tasks()
        return self.completed_tasks.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task permanently.
        Args:
            task_id: Task ID
        Returns:
            True if task was deleted, False otherwise
        """
        task = self.find_task(task_id)
        if not task:
            return False

        if task_id in self.tasks:
            del self.tasks[task_id]
        elif task_id in self.completed_tasks:
            del self.completed_tasks[task_id]
        
        self.save_tasks()
        return True

    def update_task(self, task_id: str, **kwargs) -> Optional[Dict]:
        """
        Update task properties.
        Args:
            task_id: Task ID
            **kwargs: Task properties to update
        Returns:
            Updated task or None if not found
        """
        task = self.find_task(task_id)
        if not task:
            return None

        # Validate and update each parameter
        for key, value in kwargs.items():
            if key == "description":
                if value:
                    task["description"] = value.strip()
                else:
                    raise ValueError("Task description cannot be empty")
            elif key == "priority":
                if 1 <= value <= 5:
                    task["priority"] = value
                else:
                    raise ValueError("Priority must be between 1 and 5")
            elif key == "due_date":
                parsed_due_date = None
                if value:
                    try:
                        parsed_due_date = datetime.strptime(
                            value, "%Y-%m-%d").date()
                        if parsed_due_date < datetime.now().date():
                            raise ValueError(
                                "Due date cannot be in past")
                    except ValueError:
                        raise ValueError(
                            "Invalid due date format. Use YYYY-MM-DD")
                task["due_date"] = parsed_due_date.isoformat() if parsed_due_date else None
            elif key == "project":
                task["project"] = value
            elif key == "context":
                task["context"] = value
            elif key == "recurring":
                task["recurring"] = value
            else:
                raise KeyError(f"Invalid task property: {key}")

        task["updated_at"] = datetime.now().isoformat()
        self.save_tasks()
        return task

    def list_tasks(self, 
                   filter_: Optional[str] = None, 
                   status: str = "all", 
                   priority: Optional[int] = None, 
                   project: Optional[str] = None, 
                   context: Optional[str] = None, 
                   due_soon: bool = False, 
                   sort: str = "priority") -> List[Dict]:
        """
        List tasks with filtering and sorting.
        Args:
            filter_: Filter query (searches description)
            status: Task status ('all', 'active', 'completed')
            priority: Filter by priority level
            project: Filter by project
            context: Filter by context
            due_soon: Show tasks due soon (within 3 days)
            sort: Sort field ('priority', 'due_date', 'created_at')
        Returns:
            List of matching tasks
        """
        tasks = []
        
        # Determine which tasks to include based on status
        if status == "all":
            tasks_dict = self.tasks.copy()
            tasks_dict.update(self.completed_tasks)
        elif status == "active":
            tasks_dict = self.tasks.copy()
        elif status == "completed":
            tasks_dict = self.completed_tasks.copy()
        else:
            tasks_dict = self.tasks.copy()
            tasks_dict.update(self.completed_tasks)

        # Apply filters
        filtered_tasks = []
        now = datetime.now().date()
        
        for task_id, task in tasks_dict.items():
            # Date checks
            due_date = task.get("due_date")
            parsed_due_date = None
            if due_date:
                try:
                    parsed_due_date = datetime.strptime(
                        due_date, "%Y-%m-%d").date()
                except ValueError:
                    parsed_due_date = None

            # Check due_soon criterion
            if due_soon:
                due_soon_date = now + timedelta(days=3)
                if parsed_due_date and parsed_due_date <= due_soon_date:
                    filtered_tasks.append(task)
                continue

            # Check if task meets all filtering criteria
            if filter_ and filter_.lower() not in task["description"].lower():
                continue
            
            if priority is not None and task["priority"] != priority:
                continue
            
            if project and task.get("project") != project:
                continue
            
            if context and task.get("context") != context:
                continue
            
            filtered_tasks.append(task)

        # Sort tasks
        if sort == "priority":
            filtered_tasks.sort(key=lambda x: x["priority"], reverse=True)
        elif sort == "due_date":
            filtered_tasks.sort(key=lambda x: (x.get("due_date"), x["priority"])
                               if x.get("due_date") else (now + timedelta(days=365), 0),
                              reverse=True)
        elif sort == "created_at":
            filtered_tasks.sort(key=lambda x: x["created_at"], reverse=True)

        return filtered_tasks

    def find_task(self, task_id: str) -> Optional[Dict]:
        """
        Find a task by ID.
        Args:
            task_id: Task ID
        Returns:
            Task if found, None otherwise
        """
        if task_id in self.tasks:
            return self.tasks[task_id]
        elif task_id in self.completed_tasks:
            return self.completed_tasks[task_id]
        return None

    def get_overdue_tasks(self) -> List[Dict]:
        """
        Get all overdue tasks.
        Returns:
            List of overdue tasks
        """
        overdue_tasks = []
        now = datetime.now().date()
        
        for task_id, task in self.tasks.items():
            due_date = task.get("due_date")
            if due_date:
                try:
                    parsed_due_date = datetime.strptime(
                        due_date, "%Y-%m-%d").date()
                    if parsed_due_date < now:
                        overdue_tasks.append(task)
                except ValueError:
                    # Skip tasks with invalid due dates
                    continue

        return overdue_tasks

    def get_tasks_by_priority(self, priority: int) -> List[Dict]:
        """
        Get tasks by priority level.
        Args:
            priority: Priority level (1-5)
        Returns:
            List of tasks with matching priority
        """
        if 1 <= priority <= 5:
            return [task for task in self.tasks.values()
                   if task["priority"] == priority]
        return []

    def generate_summary(self) -> str:
        """
        Generate a summary of the todo list.
        Returns:
            Summary string
        """
        summary = [
            "=== TODO LIST SUMMARY ===",
            f"\nTotal tasks: {len(self.tasks)}",
            f"Active tasks: {len(self.tasks)}",
            f"Completed tasks: {len(self.completed_tasks)}",
            f"Overdue tasks: {len(self.get_overdue_tasks())}",
        ]

        for priority in range(5, 0, -1):
            priority_tasks = self.get_tasks_by_priority(priority)
            if priority_tasks:
                summary.append(f"\nPriority {priority}:")
                for task in priority_tasks:
                    summary.append(f"  - {task["description"][:50]}..." if len(task["description"] > 50) else f"  - {task["description"]}")

        return "\n".join(summary)

    def __str__(self) -> str:
        return self.generate_summary()

if __name__ == "__main__":
    # Example usage
    todo = TodoList("todo.json")
    
    # Create some tasks
    todo.create_task("Write project proposal", priority=5, due_date="2026-11-10")
    todo.create_task("Review pull request #123", priority=4, due_date="2026-11-08")
    todo.create_task("Team meeting at 10 AM", priority=2, due_date="2026-11-09")
    todo.create_task("Client call at 2 PM", priority=3, due_date="2026-11-09")
    
    # Complete a task
    todo.complete_task("1")
    
    # Update a task
    todo.update_task("2", description="Review pull request #124", due_date="2026-11-11")
    
    # List all tasks
    print("\nAll tasks:")
    for task in todo.list_tasks():
        print(task)
    
    # Print summary
    print("\nSummary:")
    print(todo)