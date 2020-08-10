from dotenv import load_dotenv
from pathlib import Path


# enabling environment variables support via .env file
def boot():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
