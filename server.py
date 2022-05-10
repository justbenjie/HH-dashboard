from controller import Controller
from fastapi import FastAPI

config_path = "settings.json"
controller = Controller(config_path)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/vacancies/{vacancy_name}")
async def get_data(vacancy_name: str, refresh: bool = False):
    controller.update(vacancy_name)
    
    return controller.create_response(refresh)
