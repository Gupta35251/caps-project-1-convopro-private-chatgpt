from llama_index.llms.ollama import Ollama
from config.settings import settings

settings  = settings()
OLLAMA_URL = settings.OLLAMA_URL

# Module level cache for model and instance 

_current_model_name = None
_current_llm_instance = None

# These are used for caching let suppose user select a model so the program will
# not load the same model again and again until next model is changed

def get_ollama(model:str):
    global _current_model_name,_current_llm_instance # whatever change in these variable will also change in the global variable 
    if _current_model_name == model and _current_llm_instance is not None:
        return _current_llm_instance
    llm = Ollama(base_url = OLLAMA_URL,model = model,request_timeout = 120)
    _current_model_name = model
    _current_llm_instance = llm
    return llm


