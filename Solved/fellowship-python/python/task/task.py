"""This module provides the Task model-controller."""
# task/task.py
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import json
from task import DB_READ_ERROR, ID_ERROR
from task.database import DatabaseHandler

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a task from the database using its id or index."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            lis=[]
            ulis=[]
            for i in read.todo_list:
                desc, priority, don=i.values()
                if(don==False):
                    lis.append(i)
                else:
                    ulis.append(i)
            todo = lis.pop(todo_id - 1)
            lis=lis+ulis
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        lis.sort(key=lambda x: x["Priority"])
        lis.sort(key=lambda x: x["Done"])
        write = self._db_handler.write_todos(lis)
        return CurrentTodo(todo, write.error)
    
    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set a task as done."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Done"] = True
        read.todo_list.sort(key=lambda x: x["Priority"])
        read.todo_list.sort(key=lambda x: x["Done"])
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current task list."""
        read = self._db_handler.read_todos()
        return read.todo_list
        
    def add(self, description: List[str], priority: int ) -> CurrentTodo:
        """Add a new task to the database."""
        description_text = " ".join(description)
        # if not description_text.endswith("."):
        #     description_text += "."
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        read.todo_list.sort(key=lambda x: x["Priority"])
        read.todo_list.sort(key=lambda x: x["Done"])
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)