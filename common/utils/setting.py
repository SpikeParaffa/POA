from exchange.model import Settings
from functools import lru_cache
from pydantic import BaseSettings
import os

def find_env_file():
    current_path = os.path.abspath(__file__)
    while True:
        parent_path = os.path.dirname(current_path)
        env_path = os.path.join(parent_path, ".env")
        dev_env_path = os.path.join(parent_path, ".env.dev")
        if os.path.isfile(dev_env_path):
            return dev_env_path
        elif os.path.isfile(env_path):
            return env_path
        if parent_path == current_path:
            break
        current_path = parent_path
    return None

env_path = find_env_file()

class Settings(BaseSettings):
    PASSWORD: str
    WHITELIST: list[str] | None = None
    PORT: int | None = None
    DISCORD_WEBHOOK_URL: str | None = None
    UPBIT_KEY: str | None = None
    UPBIT_SECRET: str | None = None
    BINANCE_KEY: str | None = None
    BINANCE_SECRET: str | None = None
    BYBIT_KEY: str | None = None
    BYBIT_SECRET: str | None = None
    BITGET_KEY: str | None = None
    BITGET_SECRET: str | None = None
    BITGET_PASSPHRASE: str | None = None
    OKX_KEY: str | None = None
    OKX_SECRET: str | None = None
    OKX_PASSPHRASE: str | None = None
    KIS1_ACCOUNT_NUMBER: str | None = None
    KIS1_ACCOUNT_CODE: str | None = None
    KIS1_KEY: str | None = None
    KIS1_SECRET: str | None = None
    KIS2_ACCOUNT_NUMBER: str | None = None
    KIS2_ACCOUNT_CODE: str | None = None
    KIS2_KEY: str | None = None
    KIS2_SECRET: str | None = None
    KIS3_ACCOUNT_NUMBER: str | None = None
    KIS3_ACCOUNT_CODE: str | None = None
    KIS3_KEY: str | None = None
    KIS3_SECRET: str | None = None
    KIS4_ACCOUNT_NUMBER: str | None = None
    KIS4_ACCOUNT_CODE: str | None = None
    KIS4_KEY: str | None = None
    KIS4_SECRET: str | None = None
    DB_ID: str = "poa@admin.com"
    DB_PASSWORD: str = "poabot!@#$"

    class Config:
        env_file = env_path  # ".env"
        env_file_encoding = "utf-8"
        

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()


