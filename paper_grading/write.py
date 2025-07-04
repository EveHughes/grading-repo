#### Preamble ####
# Purpose: Process and output GPT4.0 grading response to .csv format.
# Author: Evelyn Hughes
# Date: 04 July 2025
# Contact: evelyn.hughes@utoronto.ca
# Pre-requisites: 
  # - `polars` must be installed (pip install polars)

from pathlib import Path
import polars as pl
from datetime import datetime

#outputs result into csv
def to_response_csv(numerical_result, comment_result):
    dic = [
        {"criterion": crit, "grade": numerical_result.get(crit), "comment": comment_result.get(crit)}
        for crit in numerical_result
    ]
    df = pl.DataFrame(dic)
    time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    path = Path(__file__).parent.parent / (f"result/responses/{time}_response.csv")
    df.write_csv(path)

#handles reading in history csv, may be empty
def read_history_csv(categories):
    path = Path(__file__).parent.parent / ("result/history.csv")
    try:
        df = pl.read_csv(path)
        # do some transformation with the dataframe
        df = df.to_dict()
    except:
        # return an empty dataframe
        df = dict()
        for category in categories:
            df[category] = []
        df["Total"] = []
    return df

#updates history csv
def update_history_csv(numerical_result):
    categories = list(numerical_result.keys())
    df = read_history_csv(categories)

    total = 0
    for category in categories:
        score = int(numerical_result[category])
        df[category].append(score)
        total += score
    df["Total"].append(total)

    path = Path(__file__).parent.parent / ("result/history.csv")
    df = pl.DataFrame(df)
    df.write_csv(path)