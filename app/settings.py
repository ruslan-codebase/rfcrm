from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_DRIVER: str = "asyncpg"
    POSTGRES_PORT: str = "5432"

    @property
    def postgres_dsn(self) -> PostgresDsn:
        dsn = (
            f"postgresql+{self.POSTGRES_DRIVER}"
            f"://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )
        return dsn


settings = Settings()