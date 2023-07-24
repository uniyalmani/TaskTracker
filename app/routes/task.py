from fastapi import APIRouter, Depends, Body, status, HTTPException, Path
from typing import List, Dict, Union
from app.models.request_models import TaskCreate, BulkTaskCreate, BulkTaskDelete, EditTask
from pydantic import  Field
from app.repository.task_repo import TasksRepository
from sqlalchemy.orm import Session
from app.utilities.helpers import get_db
from fastapi.responses import JSONResponse



router = APIRouter()



@router.get("/v1/tasks")
def get_all_task(db: Session = Depends(get_db), tasks_repo: TasksRepository = Depends()):
    try:
        all_tasks = tasks_repo.get_all_tasks(db=db)
        tasks_response = [
            {
                "id": task.id,
                "title": task.title,
                "is_completed": task.is_completed
            }
            for task in all_tasks
        ]

        # Return the response
        return {"tasks": tasks_response}
    except Exception as e:
        return {"error": e}




@router.get("/v1/tasks/{id}")
def get_task_by_id(id: int, db: Session = Depends(get_db), tasks_repo: TasksRepository = Depends()):
    try:
        # Get the task by ID using the repository method
        task = tasks_repo.get_task_by_id(db, id)

        # If the task with the given ID does not exist, raise an HTTPException with 404 status code
        if not task:
            error_msg = {"error": "There is no task at that id"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)

        # Return the task in the response format
        return task
        
    except Exception as e:
        return {"error": e}



@router.delete("/v1/tasks/{id}")
def delete_task_by_id(id: int, db: Session = Depends(get_db), tasks_repo: TasksRepository = Depends()):
    try:
        #None (return a 204 code)
        task_deleted = tasks_repo.delete_task(db, id)
        return JSONResponse( content={}, status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return {"error": e}


@router.delete("/v1/tasks")
def delete_tasks_bulk(
    tasks: BulkTaskDelete, db: Session = Depends(get_db), tasks_repo: TasksRepository = Depends()
):
    try:
        task_ids = [task.id for task in tasks.tasks]
        tasks_deleted = tasks_repo.delete_multiple_tasks(db, task_ids)
        
        return JSONResponse( content={}, status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return {"error": e}


# Endpoint to edit task by ID
@router.put("/v1/tasks/{id}")
def edit_task_by_id(
    id: int = Path(..., title="Task ID"),
    edit_info: EditTask = Body(...),
    db: Session = Depends(get_db),
    tasks_repo: TasksRepository = Depends(),
):
    try:
        task = tasks_repo.edit_task(db, id,edit_info.title, edit_info.is_completed)
        if not task:
            raise HTTPException(status_code=404, detail="There is no task at that id")
        
        return JSONResponse( content={}, status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return {"error": e}





@router.post("/v1/tasks")
def create_tasks(tasks: Union[TaskCreate, BulkTaskCreate] = Body(...), db: Session = Depends(get_db), tasks_repo: TasksRepository = Depends()):
    try:
        if isinstance(tasks, BulkTaskCreate):
            # Create multiple tasks
            created_tasks = tasks_repo.create_multiple_tasks(db, tasks.tasks)

            # Convert the created tasks to the response format
            response_tasks = [{"id": task.id} for task in created_tasks]
            return JSONResponse(content={"tasks": response_tasks}, status_code=status.HTTP_201_CREATED)

        elif isinstance(tasks, TaskCreate):
            # Create a single task
            created_task = tasks_repo.create_task(db, tasks.title)

            # Return the single task's id in the response
            return JSONResponse(content={"id": created_task.id}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return {"error": e}




