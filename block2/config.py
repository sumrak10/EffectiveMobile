from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env')

    BASE_URL: str = 'https://spimex.com'
    DATETIME_FORMAT: str = '%d.%m.%Y'

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASS: str = 'vErY26hhh03PSWD'
    DB_NAME: str = 'anocat_db'
    DB_AND_DRIVER: str = "postgresql+asyncpg"
    @property
    def DB_DSN(self):
        return f"{self.DB_AND_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
