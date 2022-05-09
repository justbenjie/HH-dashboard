import json
import requests
from typing import Dict

   
class Exchanger:
    __EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6/4f44d7ad6be4d970e8ecc92e/latest/USD/"
    
    def __init__(self, config_path: str):
        self.config_path = config_path

    def update_exchange_rates(self, rates: Dict) -> Dict:
        """Scrape exchange rates and save them in rates dictionary

        Args:
            rates (Dict): dictionary of currencies and their exchange rates

        Return:
            Dict: updated rates
        """
        

        try: 
            response = requests.get(self.__EXCHANGE_RATE_URL).json()
            
            new_rates = response["conversion_rates"]
        except requests.exceptions.ConnectionError:
            print("Exchange rates can't be updated without internet connection!")

        for currencies in rates:
            rates[currencies] = new_rates[currencies]

        rates["RUR"] = rates.pop("RUB")

        with open(self.config_path, "r") as cfg:
            settings = json.load(cfg)

        settings["conversion_rates"] = rates

        with open(self.config_path, "w") as cfg:
            json.dump(settings, cfg, indent=2)

        return rates


if __name__ == "__main__":

    exchanger = Exchanger("settings.json")
    config_rates = { "USD": None, "BYN": None, "RUB": None, "EUR": None, "UAH": None}
    exchanger.update_exchange_rates(config_rates)
