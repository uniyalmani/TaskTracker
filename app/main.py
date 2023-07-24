from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import create_engine
from .models.database_models import Base, Tasks
from .controllers.database_initializer import engine
from .utilities.helpers import get_db
from .routes import task

app = FastAPI()



# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(task.router)