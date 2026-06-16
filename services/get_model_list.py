from config.settings import settings

settings = settings()

def get_ollama_model_list():
    model_list = settings.OLLAMA_MODELS
    model_names = [model.strip() for model in model_list.split(",") if model.strip()]
    # strip() func is used to remove \n \t and if model.strip() is used to only keep the items or elements which are not empty if after separating by comam there are expty fields left so if model.strip() will remoove them from model_names
    return model_names


