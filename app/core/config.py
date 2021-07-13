from typing import Optional

from pydantic import BaseSettings, Field


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # This variable will be loaded from the .env file. However, if there is a
    # shell environment variable having the same name, that will take precedence.

    # the class Field is necessary while defining the global variables
    ENV_STATE: Optional[str] = Field(..., env="ENV_STATE")

    SECRET_KEY: Optional[str] = Field(..., env="SECRET_KEY")
    POSTGRES_USER: Optional[str] = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_SERVER: Optional[str] = Field(..., env="POSTGRES_SERVER")
    POSTGRES_PORT: Optional[str] = Field(..., env="POSTGRES_PORT")
    POSTGRES_DB: Optional[str] = Field(..., env="POSTGRES_DB")
    APPLICATION_ID: Optional[str] = Field(..., env="APPLICATION_ID")
    APPLICATION_ROOT: Optional[str] = Field(..., env="APPLICATION_ROOT")

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


config = GlobalConfig()
# print(config.__repr__())
