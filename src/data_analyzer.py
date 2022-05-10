import pandas as pd
import numpy as np
from typing import List
import itertools

class Analyser:
    @staticmethod
    def find_top_skills(skills: List) -> List:
        """Find top 10 skills and their number of mentions

        Args:
            skills (List): skills from each vacancy

        Returns:
            List: top 10 skills
        """

        merged_skills = list(itertools.chain.from_iterable(skills))
        skilles_series = pd.Series(merged_skills)
        skilles_series = skilles_series.apply(lambda x: x.lower().strip())

        top_skills = skilles_series.value_counts().head(10)
        return top_skills.to_dict()

    """
    @staticmethod
    def find_description_top_words(descriptions: List) -> pd.Series:

        merged_descriptions = list(itertools.chain.from_iterable(descriptions))
        merged_descriptions = merged_descriptions.apply()
    """
    
    