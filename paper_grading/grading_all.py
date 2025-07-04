#### Preamble ####
# Purpose: Grade a Donaldson Project using OpenAI's GPT-4 model based on a rubric -- multiple categories at a time
# Author: Evelyn Hughes
# Date: 04 July 2025
# Contact: evelyn.hughes@utoronto.ca
# Pre-requisites: 
  # - `openai` must be installed (pip install openai)
  # - `key.txt' file must be create and contain valid OpenAI API key

import openai
from pathlib import Path
import re
import pandas as pd
from datetime import datetime

from read import read_project, read_prompt, read_rubric
from write import update_history_csv


### GRADING FILES ###
#grades a single component (scripts or paper) using OpenAI's GPT model -- later update to have prompt be from txt file
def grade_component(project_component, rubric, prompt):
    client = openai.OpenAI(api_key = my_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", 
             "content": prompt   # prompt provides basic role & instructions
            },
            {"role": "user",
             "content": f"""
                project: {project_component}
                rubric: {rubric}
                For each criterion, return a row in CSV format with:
                Rubric Category, Score, Justification

                Output CSV with a header row and one row per criterion.
                Use this format:
                Criterion, Score, Justification
                abstract.txt, 4, "Clear and structured presentation"
                authordaterepo.txt, ...

                Only return the CSV — no commentary or explanation." """
            }
        ],
        max_tokens = 300
    )
    return response.choices[0].message.content

#parses response from grader into dataframe with columns: Criterion, Score, Justification
def gpt_output_to_dataframe(gpt_output):
    rows = []
    lines = gpt_output.strip().split("\n")

    for line in lines:
        match = re.match(r"Criterion (\d+):.*?;\s*(\d+);\s*(.*)", line)
        if match:
            rows.append({
                "Criterion": int(match.group(1)),
                "Score": int(match.group(2)),
                "Justification": match.group(3).strip()
            })

    return pd.DataFrame(rows)

## AUTOGRADING ##
#goes through rubric and grades -- later divide rubric folder into scripts and paper
def grade(project_name):
    #reads in the files
    rubric = read_rubric()
    prompt = read_prompt(1)
    project = read_project(project_name)

    #calls the grader for scripts
    print("Grading scripts...")
    scripts_rubric = {k: v for k, v in rubric.items() if k in ['tests.txt', 'reporoducuble.txt']}
    response = grade_component(project["Scripts"], str(scripts_rubric), prompt)
    scripts_df = gpt_output_to_dataframe(response)
    
    #calls grader for paper
    print("Grading paper...")
    paper_rubric = rubric.copy()
    del paper_rubric['tests.txt']
    del paper_rubric['reproducible.txt']
    response = grade_component(project["Paper"], str(paper_rubric), prompt)
    paper_df = gpt_output_to_dataframe(response)

    #combines data frames & adds the total score 
    final_df = pd.concat([scripts_df, paper_df], ignore_index=True)

    total_score = final_df["Score"].sum()

    total_score_row = {
        "Criterion": "Total",
        "Score": total_score,
        "Justification": "Sum of all rubric scores",
    }
    final_df = final_df.append(total_score_row, ignore_index=True)

    #outputs results
    time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    path = Path(__file__).parent.parent / (f"result/responses/{time}_response.csv")
    final_df.to_csv(path, index=False)

    #updates history csv
    #update_history_csv(final_df)
    

if __name__ == "__main__":
   #get key
    with open('key.txt', 'r') as file:
        my_key = file.read().strip()
    
    grade("project1")