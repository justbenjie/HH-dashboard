from src.currency_convert import Exchanger
from src.data_analyzer import Analyser
from src.data_extraction import Collector
import json
from typing import Dict


class Controller:
    def __init__(self, config_path: str):
        self.exchanger = Exchanger(config_path)
        self.collector: Collector | None = None
        self.analyser: Analyser | None = None
        self.settings: Dict | None = None
        
    def update(self, vacancy_name: str | None):
        with open(self.config_path, "r") as cfg:
            self.settings = json.load(cfg)

        self.settings["conversion_rates"] = self.exchanger.update_exchange_rates(self.settings["conversion_rates"])

        if vacancy_name:
            self.settings["search_params"]["vacancy_name"] = vacancy_name
            with open(self.config_path, "w") as cfg:
                json.dump(self.settings, cfg, indent=2)

        self.collector = Collector(self.settings)

    def create_response(self, refresh: bool = False):
        vacancies = self.collector.get_vacancies(self.settings["search_params"], refresh)
        skills = self.analyser.find_top_skills(vacancies["Skills"])
        response = {"Skills": skills}
        for column in ["Salary", "Schedule", "Experience"]:
            response[column] = vacancies[column]
        return response
