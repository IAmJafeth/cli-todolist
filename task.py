from typing import Dict, Union
from pprint import pprint

class Task():
    tasks: Dict[int, "Task"] = {}
    __current_id: int = 0

    def __init__(self, title: str, description:str = None) -> None:
        self.id = Task.__current_id
        self.title = title
        self.description = description
        self.completed = False
    
    def __str__(self) -> str:
        return f"""\tId: {self.id}
        Title: {self.title}
        Description: {self.description if self.description else "N/A"}
        Completed: {self.completed}
        """
    def __repr__(self) -> str:
        return f"<task.Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})>"
    
    @classmethod
    def create(cls, title: str, description:str) -> "Task":
        task = Task(title,description)
        cls.tasks[task.id] = task
        cls.__current_id += 1
        return task
    
    @classmethod
    def delete(cls, id:int) -> Union[bool,"Task"]:
        if id in cls.tasks:
            task = cls.tasks[id]
            del cls.tasks[id]
            return task
        return False
    
    @classmethod
    def complete(cls, id:int) -> Union[bool,"Task"]:
        if id in cls.tasks:
            cls.tasks[id].completed = True
            return cls.tasks[id]
        return False

    @classmethod
    def list(cls) -> None:
        if cls.tasks:
            pprint(cls.tasks)
        else:
            print("No Tasks have been created yet")