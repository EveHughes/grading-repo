#### Preamble ####
# Purpose: Grade a Donaldson Project using OpenAI's GPT-4 model based on a rubric. -- one category at a time
# Author: Evelyn Hughes
# Date: 04 July 2025
# Contact: evelyn.hughes@utoronto.ca
# Pre-requisites: 
  # - `openai` must be installed (pip install openai)
  # - `key.txt' file must be create and contain valid OpenAI API key

import openai
import time
from datetime import datetime

from read import read_project, read_prompt, read_rubric
from write import update_history_csv, to_response_csv

#read in key info
with open('azure_key.txt', 'r') as file:
    lines = file.readlines()
    azure_api_key = lines[0].strip()
    azure_endpoint = lines[1].strip()

# Set up Azure OpenAI client
client = openai.AzureOpenAI(
    api_key=azure_api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=azure_endpoint
)

#grades project for a specific rubric criterion
def grade_criterion(project_component, criterion, prompt):
    response = client.chat.completions.create(
        model = "ijf-gpt-4o",
        messages=[
            {"role": "system", 
             "content": prompt
            },
            {"role": "user",
             "content": f"""
                project: {project_component}
                rubric: {criterion}
                Return first the rubric category, then only the score, and then a comment of your justification, each seperated by a semicolon."
                Do not include any additional spaces after semicolons.
                Example:
                reproducible.txt;3;The project has a clear README file with instructions for reproducing the results, but lacks a requirements.txt file for dependencies."""
            }
        ],
        max_tokens = 300
    )
    return response.choices[0].message.content

#goes through entire rubric and grades all criteria
def grade(project_name):
    #reads in the files
    rubric = read_rubric()
    prompt = read_prompt(1)
    project = read_project(project_name)

    numerical_result = {}
    comment_result = {}

    #calls the grader on each criterion in the rubric -- criterion is name of file of category in rubric folder
    for criterion in rubric:
        print(f"Grading criterion: {criterion}")
        #loop to ensure that the grading is done correctly
        while True:
            if criterion not in ["reproducible.txt", "tests.txt"]: # these criteria are only for scripts
                criterion_result = grade_criterion(project["Paper"], rubric[criterion], prompt)
            else: 
                criterion_result = grade_criterion(project["Scripts"], rubric[criterion], prompt)

            criterion_result = criterion_result.split(";")
            print(f"Criterion result: {criterion_result}")

            #prints the grade and comment & breaks, or prints an error message
            if len(criterion_result) == 3 and criterion_result[1].isnumeric():
                numerical_result[criterion] = criterion_result[1]
                comment_result[criterion] = criterion_result[2]
                print(f"Grade for {criterion}: {numerical_result[criterion]}")
                break
            elif len(criterion_result) != 3:
                print(f"Error with rubric category {criterion}, split wrong")
                time.sleep(5)
            else:
                print(f"Error with rubric category {criterion}, second entry not a number")
                time.sleep(5)
    
    #updates the csvs
    date_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    to_response_csv(date_time, numerical_result, comment_result)
    update_history_csv(date_time, numerical_result)
    return (numerical_result, comment_result)


if __name__ == "__main__":
    #get key
    with open('key.txt', 'r') as file:
        my_key = file.read().strip()
    
    result = grade("project1")
    
    #prints the numerical results
    print(result[0])