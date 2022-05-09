from controller import Controller
from fastapi import FastAPI

app = FastAPI()
config_path = "settings.json"
controller = Controller(config_path)

@app.get("items/{vacancy_name}")
async def get_data(vacancy_name: str, refresh: bool = False):
    controller.update(vacancy_name)
    
    return controller.create_response(vacancy_name, refresh)
