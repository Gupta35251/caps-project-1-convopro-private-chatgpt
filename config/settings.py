from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class settings(BaseSettings):
    OLLAMA_URL : str
    OLLAMA_MODELS : str
    MONGO_DB_URL : str
    MONGO_DB_NAME : str

# as we do from getenv to load the environment variables int the variable name 
# and use it anywhere same this we are doing so with class settings BaseSettings
# And load_dotenv() is used to load the environment variables
    class config : 
        env_file = ".env"
        env_file_encoding = 'utf-8'
# This tells from where to read the environment variables(.env) and how to read it 

# @mcp.tool():



