import pandas as pd
import numpy as np
from typing import Dict, List
import itertools

class Analyser:
    @staticmethod
    def find_top_skills(skills: List) -> Dict:
        """Find top 10 skills and their number of mentions

        Args:
            skills (List): List of lists with skills for each vacancy

        Returns:
            Dict: Top 10 skills
        """

        merged_skills = list(itertools.chain.from_iterable(skills))
        skilles_series = pd.Series(merged_skills)
        skilles_series = skilles_series.apply(lambda x: x.lower().strip())

        top_skills = skilles_series.value_counts().head(10)
        return top_skills.to_dict()

    @staticmethod
    def value_count(data: List) -> Dict:

        series = pd.Series(data)
        series = series.apply(lambda x: x.lower().strip())
        value_count = series.value_counts()
        return value_count.to_dict()

    @staticmethod
    def parse_salary(salary: List) -> List:

        merged_salary = list(itertools.chain.from_iterable(salary))
        salary_Series = pd.Series(merged_salary).dropna()
        upper_limit = salary_Series.quantile(0.99)
        lower_limit = salary_Series.quantile(0.01)
        
        processed_salary = salary_Series[(salary_Series > lower_limit) & (salary_Series < upper_limit)]
        return processed_salary.to_list()


        

    """
    @staticmethod
    def find_description_top_words(descriptions: List) -> pd.Series:

        merged_descriptions = list(itertools.chain.from_iterable(descriptions))
        merged_descriptions = merged_descriptions.apply()
    """
    
    