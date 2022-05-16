import json
import requests
from typing import Dict
from pathlib import Path
   
class Exchanger:
    __EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6/4f44d7ad6be4d970e8ecc92e/latest/USD/"

    def __init__(self):
        self.config_path = Path("settings.json") 

    def update_exchange_rates(self) -> Dict:
        """Scrape exchange rates and save them in rates dictionary

        Return:
            Dict: updated rates
        """

        try: 
            response = requests.get(self.__EXCHANGE_RATE_URL).json()
            
            new_rates = response["conversion_rates"]
            rates = { "BYN": None, "USD": None, "RUB": None, "EUR": None, "UAH": None}

            for currencies in rates:
                rates[currencies] = new_rates[currencies]

            rates["RUR"] = rates.pop("RUB")
            rates["BYR"] = rates.pop("BYN")

            with open(self.config_path, "r") as cfg:
                settings = json.load(cfg)

            settings["conversion_rates"] = rates

            with open(self.config_path, "w") as cfg:
                json.dump(settings, cfg, indent=2)

            return rates
            
        except requests.exceptions.ConnectionError:
            print("\nExchange rates can't be updated without internet connection!\n")
            

        


if __name__ == "__main__":

    exchanger = Exchanger()
    exchanger.update_exchange_rates()
