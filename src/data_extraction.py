# import libraries
import requests
import pandas as pd
import json
import time

params = {
        'text': f'NAME:{request}',
        'area': 16,
        'page': 0,
        'per_page': 100
    }


class DataCollector:
    __BASE_URL = "https://api.hh.ru/vacancies/"

    __DICT_KEYS = (
        'id',
        'name',
        'salary'
    )

    __EXC_RATE = {
        
    }

    @staticmethod
    def __convert_gross(is_gross: bool) -> float:
        return 0.87 if is_gross else 1

    def get_vacancy(self, vacancy_id: str) -> tuple:
        url = f"{self.__BASE_URL}{vacancy_id}"
        vacancy = requests.api.get(url).json()

        salary = vacancy['salary']
        from_to = {"from": None, "to": None}

        if salary:
            is_gross = salary["gross"]
            for k, v in from_to.items():
                if salary[k]:
                    _value = self.__convert_gross(is_gross)
                    from_to[k] = int(_value * salary[k] / self._exchange_rate[salary["currency"]])
        return (
            vacancy_id,
            vacancy["employer"]["name"],
            vacancy["name"],
        )

    def get_vacancies(request, page_number=0):
        response = requests.get(url, params).json()
        return response


    def get_description(request, data):
        for page in range(0, 20):
            for vacancy in get_vacancies(request, page)['items']:
                vacancy_id = vacancy['id']
                name = vacancy['name'].lower()
                if not vacancy['salary']:
                    salary_from, salary_to, currency = None, None, None
                else:
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']
                    currency = vacancy['salary']['currency']

                salary = vacancy['salary']
                schedule = vacancy['schedule']['name'].lower()
                requirement = vacancy['snippet']['requirement'].lower()
                location = vacancy['area']['name']
                # save data in pandas df

                data = data.append({"id": vacancy_id, "name": name,
                                    "salary_from": salary_from, "salary_to": salary_to,
                                    "currency": currency, "schedule": schedule,
                                    "requirement": requirement, "location": location},
                                   ignore_index=True)
            # check if page is last
            if get_vacancies('data', page)['pages'] - page < 2:
                break
        return data


    def create_csv(request):
        df = pd.DataFrame(
            columns=["id", "name", "salary_from", "salary_to",
                     "currency", "schedule", "requirement", "location"])
        df = get_description(request, df)
        df.to_csv('channel_info.csv')
