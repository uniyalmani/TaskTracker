from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., example="title for the task")
    is_completed: Optional[bool] = False




class BulkTaskCreate(BaseModel):
    tasks: List[TaskCreate]



class EditTask(TaskCreate):
    title: str = Field(..., example="new title")
        
class TaskID(BaseModel):
    id: int


class BulkTaskDelete(BaseModel):
    tasks: List[TaskID]
