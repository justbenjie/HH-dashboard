from src.currency_convert import Exchanger
from src.data_analyzer import Analyser
from src.data_collector import Collector
import json
from typing import Dict
import pandas as pd


class Controller:
    def __init__(self, config_path: str):
        self.exchanger = Exchanger()
        self.analyser = Analyser()
        self.collector: Collector | None = None
        self.settings: Dict | None = None
        self.config_path = config_path
        
    def update(self, vacancy_name: str | None):
        with open(self.config_path, "r") as cfg:
            self.settings = json.load(cfg)

        self.exchanger.update_exchange_rates()
        if vacancy_name:
            self.settings["search_params"]["text"] = vacancy_name

        with open(self.config_path, "w") as cfg:
            json.dump(self.settings, cfg, indent=2)

        self.collector = Collector()

    def create_response(self, refresh: bool = False):
        vacancies = self.collector.collect_vacancies(refresh)

        df = pd.DataFrame(data=vacancies)
        df.to_excel('logging.xlsx', index=False)

        count = len(vacancies["Id"])
        skills = self.analyser.find_top_skills(vacancies["Skills"])
        salary = self.analyser.parse_salary_by_experience(vacancies["From"], vacancies["To"], vacancies["Experience"])
        response = {"Count": count, "Skills": skills, "Salary": salary}
        for column in ["Schedule", "Experience"]:
            response[column] = self.analyser.value_count(vacancies[column])
        #print(response)
        return response
