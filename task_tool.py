import os
import json
import datetime
from pathlib import Path

# Simple file-based task storage
TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

def _load_tasks():
    """Load tasks from file or initialize empty task list."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"tasks": []}
    else:
        return {"tasks": []}

def _save_tasks(tasks_data):
    """Save tasks to file."""
    Path(TASKS_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks_data, f, indent=2)

def add_task(title, description="", due_date=None, priority="medium"):
    """
    Add a new task.
    
    Args:
        title (str): Task title
        description (str, optional): Task description. Defaults to "".
        due_date (str, optional): Due date in YYYY-MM-DD format. Defaults to None.
        priority (str, optional): Task priority (low, medium, high). Defaults to "medium".
    
    Returns:
        dict: Added task info
    """
    tasks_data = _load_tasks()
    
    # Generate a new task ID
    task_id = 1
    if tasks_data["tasks"]:
        task_id = max(task["id"] for task in tasks_data["tasks"]) + 1
    
    # Validate due date format if provided
    if due_date:
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid due date format. Please use YYYY-MM-DD."}
    
    # Validate priority
    if priority not in ["low", "medium", "high"]:
        return {"error": "Invalid priority. Please use low, medium, or high."}
    
    # Create new task
    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    
    tasks_data["tasks"].append(new_task)
    _save_tasks(tasks_data)
    
    return {"success": True, "task": new_task}

def get_tasks(filter_type=None):
    """
    Get tasks with optional filtering.
    
    Args:
        filter_type (str, optional): Filter type (all, active, completed). Defaults to None.
    
    Returns:
        dict: Tasks matching the filter
    """
    tasks_data = _load_tasks()
    
    if not filter_type or filter_type == "all":
        return {"tasks": tasks_data["tasks"]}
    
    if filter_type == "active":
        filtered = [task for task in tasks_data["tasks"] if not task["completed"]]
        return {"tasks": filtered}
    
    if filter_type == "completed":
        filtered = [task for task in tasks_data["tasks"] if task["completed"]]
        return {"tasks": filtered}
    
    return {"error": "Invalid filter type. Please use all, active, or completed."}

def update_task(task_id, updates):
    """
    Update a task.
    
    Args:
        task_id (int): Task ID to update
        updates (dict): Updates to apply to the task
    
    Returns:
        dict: Updated task info
    """
    tasks_data = _load_tasks()
    
    # Find the task to update
    for i, task in enumerate(tasks_data["tasks"]):
        if task["id"] == task_id:
            # Update fields
            for key, value in updates.items():
                if key in task and key != "id":  # Prevent ID from being changed
                    task[key] = value
            
            _save_tasks(tasks_data)
            return {"success": True, "task": task}
    
    return {"error": f"Task with ID {task_id} not found."}

def delete_task(task_id):
    """
    Delete a task.
    
    Args:
        task_id (int): Task ID to delete
    
    Returns:
        dict: Operation result
    """
    tasks_data = _load_tasks()
    
    # Find the task to delete
    for i, task in enumerate(tasks_data["tasks"]):
        if task["id"] == task_id:
            # Remove the task
            del tasks_data["tasks"][i]
            _save_tasks(tasks_data)
            return {"success": True, "message": f"Task with ID {task_id} deleted."}
    
    return {"error": f"Task with ID {task_id} not found."}