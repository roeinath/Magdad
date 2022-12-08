from typing import Callable, Dict
from fuzzywuzzy import process


def get_closest_strings(input: str, all_options: [str] = [], limit: int = 1):
    all_options = list(all_options)
    options_fuzz = process.extractBests(input, all_options, limit=limit)
    matches = [name_sug for (name_sug, score) in options_fuzz]
    return matches
