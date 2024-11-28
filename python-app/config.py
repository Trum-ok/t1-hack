import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), override=True)

endpoint = f"{os.getenv('MINIO_HOST')}:{os.getenv('MINIO_PORT')}"
user = os.getenv("MINIO_ROOT_USER")
password = os.getenv("MINIO_ROOT_PASSWORD")
backet = os.getenv("MINIO_BACKET")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    PG_HOST = os.environ.get('PG_HOST')
    PG_PORT = os.environ.get("PG_PORT", 5432)
    PG_USER = os.environ.get('PG_USER', 'gen_user')
    PG_PASS = os.environ.get('PG_PASS')
    PG_DATA = os.environ.get('PG_DB', 'default_db')

    AI_ANTHROPIC = os.getenv("ANTHROPIC_API")
    AI_OPENAI = os.getenv("OPEN_AI_API")
    AI_GOOGLE = os.getenv("GOOGLE_API")
    AI_LLAMA = os.getenv("LLAMA_API")
