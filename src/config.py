from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}?ssl=disable"
        )
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
