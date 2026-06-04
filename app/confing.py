import os


class Config:
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "seminar_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "seminar_pass")
    DB_NAME = os.getenv("DB_NAME", "seminar_db")
