# import libraries
from concurrent.futures import ThreadPoolExecutor
import re
import requests
import pandas as pd
import json
import time
from typing import Dict
from pathlib import Path
from urllib.parse import urlencode


class DataCollector:
    __BASE_URL = "https://api.hh.ru/vacancies/"

    __DICT_KEYS = (
        "Id",
        "Name",
        "Employer",
        "Salary",
        "From",
        "To",
        "Experience",
        "Schedule",
        "Skills",
        "Requirement",
        "Location"
    )

    __CACHE_DIR = Path("cached_data")

    def __init__(self, exchange_rates: Dict):
        self._exchange_rates = exchange_rates
    
    @staticmethod 
    def clean_tags(raw_text: str) -> str:
        """Remove HTML tags from text

        Args:
            raw_text (str): Raw string with HTML tags

        Returns:
            str: Processed string
        """

        pattern = re.compile("<.*?>")
        return re.sub(pattern, "", raw_text)
 
    @staticmethod
    def convert_gross(is_gross: bool) -> float:
        """Calculate clear salary (net)

        Args:
            is_gross (bool): True if gross salary is given

        Returns:
            float: Net salary coefficient
        """

        return 0.87 if is_gross else 1

    def get_vacancy(self, vacancy_id: str) -> tuple:
        url = f"{self.__BASE_URL}{vacancy_id}"
        vacancy = requests.api.get(url).json()
        try:
            salary = vacancy['salary']
        except KeyError:
            salary = None
        from_to = {"from": None, "to": None}
        
        if salary:
            if salary["currency"] == "RUR":
                salary["currency"] = "RUB"
            is_gross = salary["gross"]
            for k in from_to:
                if salary[k]:
                    _value = self.convert_gross(is_gross)
                    from_to[k] = int(_value * salary[k] / self._exchange_rates[salary["currency"]])
        try:
            return (
                vacancy_id,
                vacancy["name"],
                vacancy["employer"]["name"],
                salary is not None,
                from_to["from"],
                from_to["to"],
                vacancy["experience"]["name"],
                vacancy["schedule"]["name"],
                [skill["name"] for skill in vacancy["key_skills"]],
                self.clean_tags(vacancy["description"]),
                vacancy['area']['name']
            )
        except: pass

    def collect_vacancies(self, params: Dict, refresh: bool = False) -> Dict:
        """Parse vacancy description

        Args:
            params (Dict): Search parametrs for GET request
            refresh (bool, optional): Refresh cached data. Defaults to False.

        Returns:
            Dict: Dict of vacancy descriptions
        """

        # load cached data
        cache_file = Path(self.__CACHE_DIR, "cache.json")
        vacancy_name: str = params.get("text")
        try:
            cached_vacancies = json.load(open(cache_file, 'r'))
        except (json.decoder.JSONDecodeError):
            cached_vacancies = {}

        # return cached vacancies if refresh if False
        if not refresh:
            try:
                if vacancy_name in cached_vacancies:
                    return cached_vacancies[vacancy_name]
            except(FileNotFoundError):
                pass

        
        # get number of pages
        url = self.__BASE_URL + "?" + urlencode(params)
        number_pages = requests.get(url).json()["pages"]

        # get each vacancy index
        vacancy_inds = []
        for ind in range(number_pages+1):
            response = requests.get(url, {"page": ind}).json()
            if "items" not in response:
                break
            vacancy_inds.extend(vacancy["id"] for vacancy in response["items"])

        # parse vacancies by their indexes
        vacancies = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            for vacancy in executor.map(self.get_vacancy, vacancy_inds):
                vacancies.append({vacancy})
        

        cached_vacancies[vacancy_name] = vacancies
        json.dump(cached_vacancies, open(cache_file, "w"), indent=2)


if __name__ == "__main__":
    dc = DataCollector(exchange_rates={"USD": 1, "BYN": 2.815, "RUB": 68.6863, "EUR": 0.9498, "UAH": 29.6342})

    vacancies = dc.collect_vacancies(
        params={"text": "Python", "area": 1, "per_page": 50},
        # refresh=True
    )
    print(vacancies)