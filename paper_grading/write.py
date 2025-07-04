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

## RESPONSE CSV ##

#outputs result into csv
def to_response_csv(time, numerical_result, comment_result):
    dic = [
        {"Criterion": crit, "Score": int(numerical_result.get(crit)), "Comment": comment_result.get(crit)}
        for crit in numerical_result
    ]
    df = pl.DataFrame(dic)

    # adds total score row
    total_score = df["Score"].sum()
    total_score_row = pl.DataFrame({
        "Criterion": "Total",
        "Score": total_score,
        "Comment": "Sum of all rubric scores",
    })
    
    df = pl.concat([df, total_score_row], how="vertical")
    path = Path(__file__).parent.parent / (f"result/responses/{time}_response.csv")
    df.write_csv(path)

## HISTORY CSV ##

#handles reading in history csv, may be empty; returns dictionary
def read_history_csv(categories):
    path = Path(__file__).parent.parent / ("result/history.csv")
    try:
        df = pl.read_csv(path)
        df = df.to_dict()
    except:
        # return an dictionary with empty lists if the history csv does not exist
        df = dict()
        for category in categories:
            df[category] = []
        df["Total"] = []
        df["Time"] = []
    return df

#updates history csv
def update_history_csv(time, numerical_result): 
    categories = list(numerical_result.keys())
    df = read_history_csv(categories)
   
    df["Time"].append(time)
    for cat in categories:
        df[cat].append(int(numerical_result[cat]))
    df["Total"].append(sum(int(numerical_result[cat]) for cat in categories))

    path = Path(__file__).parent.parent / ("result/history.csv")
    df = pl.DataFrame(df)
    df.write_csv(path)