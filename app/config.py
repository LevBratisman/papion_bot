from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    BOT_TOKEN: str
    ADMIN_ID: int
    FB_CHAT_ID: str
    
    PROXY_API_KEY: str
    
    DB_URL: str

    @property
    def OPENAI_BASE_URL(self):
        return f"https://api.proxyapi.ru/openai/v1"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()