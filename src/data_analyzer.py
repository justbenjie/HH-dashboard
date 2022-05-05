import pandas as pd
import numpy as np
from typing import List
import itertools

class Analyser:
    def find_top_skills(skills: pd.Series) -> pd.Series:
        """Find the most common skills in vacancies 

        Args:
            skills (List): List of skills for every vacancy

        Returns:
            List: Sorted unique skills
        """

        merged_skills = list(itertools.chain.from_iterable(skills))
        skilles_series = pd.Series(merged_skills)
        skilles_series = skilles_series.apply(lambda x: x.lower().strip())

        top_skills = skilles_series.value_counts()
        return top_skills

    