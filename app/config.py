import os
from pydantic import BaseSettings

class AppSettings(BaseSettings):
    mysql_username: str = os.getenv("MYSQL_USER", default="")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", default="")
    mysql_host: str = os.getenv("MYSQL_ROOT_HOST", default="")
    mysql_port: str = os.getenv("MYSQL_PORT", default="")
    mysql_database: str = os.getenv("MYSQL_DATABASE", default="")

    def get_db_url(self) -> str:
        
        if all([self.mysql_username, self.mysql_password, self.mysql_host, self.mysql_port, self.mysql_database]):
            return f"mysql+mysqlconnector://{self.mysql_username}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        else:
            return "sqlite:///database.db"

    class Config:
        env_file = ".env"
