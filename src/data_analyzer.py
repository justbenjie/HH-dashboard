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
    def parse_salary_by_experience(salary_from: List, salary_to: List, experience: List) -> Dict:
        from_exp = {"Experience": experience, "Salary": salary_from}
        to_exp = {"Experience": experience, "Salary": salary_to}
        df_from = pd.DataFrame(from_exp)
        df_to = pd.DataFrame(to_exp)
        concat_df = pd.concat([df_from, df_to])
        min, max, median = concat_df["Salary"].min(), concat_df["Salary"].max(), concat_df["Salary"].median()
        """
        upper_limit = concat_df["Salary"].quantile(0.99)
        lower_limit = concat_df["Salary"].quantile(0.01)
        concat_df = concat_df[(concat_df["Salary"] > lower_limit) & (concat_df["Salary"] < upper_limit)]
        """
        concat_df = concat_df.groupby(["Experience"]).median()
        concat_df.dropna(inplace=True)
        return concat_df.to_dict()["Salary"], min, max, median

 




    """
    @staticmethod
    def find_description_top_words(descriptions: List) -> pd.Series:

        merged_descriptions = list(itertools.chain.from_iterable(descriptions))
        merged_descriptions = merged_descriptions.apply()
    """
    
    