from sqlalchemy.orm import Session
from app.models.database_models import Tasks

class TasksRepository:
    def get_task_by_id(self, db: Session, task_id: int) -> Tasks:
        return db.query(Tasks).filter(Tasks.id == task_id).first()

    def get_all_tasks(self, db: Session) -> list[Tasks]:
        return db.query(Tasks).all()

    def create_task(self, db: Session, title: str, is_completed: bool = False) -> Tasks:
        task = Tasks(title=title, is_completed=is_completed)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def edit_task(self, db: Session, task_id: int, title: str, is_completed: bool) -> Tasks:
        task = self.get_task_by_id(db, task_id)
        if task:
            task.title = title
            task.is_completed = is_completed
            db.commit()
            db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: int) -> bool:
        task = self.get_task_by_id(db, task_id)
        if task:
            db.delete(task)
            db.commit()
            return True
        return False

    def create_multiple_tasks(self, db: Session, tasks_data: list[dict[str, str]]) -> list[Tasks]:
        tasks = [Tasks(title=task.title, is_completed=task.is_completed) for task in tasks_data]
        db.add_all(tasks)
        db.commit()
        for task in tasks:
            db.refresh(task)
        return tasks

    def delete_multiple_tasks(self, db: Session, task_ids: list[int]) -> int:
        tasks_deleted = db.query(Tasks).filter(Tasks.id.in_(task_ids)).delete(synchronize_session="fetch")
        db.commit()
        return tasks_deleted
