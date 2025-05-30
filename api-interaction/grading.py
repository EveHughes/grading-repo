import openai
from pathlib import Path
import pandas as pd

CATEGORIES = ["Download", "Clean", "Comments", "Caption", "Figure", "Sentence", "Total"]

### READING IN ###
#get key
with open('key.txt', 'r') as file:
    my_key = file.read().strip()

#get prompt
def read_prompt(i):
    file_path = Path(__file__).parent / ("prompts/prompt" + str(i) + ".txt")
    with open(file_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()
    return prompt_text

#reads in rubric as a dictionary
def read_rubric():
    rubric = {}
    path = Path(__file__).parent / ("rubric")
    for file in path.iterdir():
        if file.is_file():
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    rubric[file.name] = content
            except Exception as e:
                print(f"Error reading {file.name}: {e}")
    return rubric

#reads in project -- just paper file as of now
def read_project():
    file_path = Path(__file__).parent / ("input/paper.qmd")
    with open(file_path, "r", encoding="utf-8") as f:
        paper_text = f.read()
    return paper_text

### GRADING FILES ###
#grades project for a specific criterion
def grade_criterion(project, criterion, prompt):
    client = openai.OpenAI(api_key = my_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", 
             "content": prompt
            },
            {"role": "user",
             "content": f"""
                project: {project}
                rubric: {criterion}
                Return first the rubric category, then the score, and then a comment of your justification, each seperated by a semicolon." """
            }
        ],
        max_tokens = 300
    )
    return response.choices[0].message.content

#goes through entire rubric and grades
def grade():
    rubric = read_rubric()
    prompt = read_prompt(1)
    project = read_project()

    numerical_result = {}
    comment_result = {}
    for criterion in rubric:
        criterion_result = grade_criterion(project, rubric[criterion], prompt)
        criterion_result = criterion_result.split(";")

        if len(criterion_result) == 3 and criterion_result[1].isnumeric():
            numerical_result[criterion_result[0]] = criterion_result[1]
            comment_result[criterion_result[0]] = criterion_result[2]
            print(criterion_result[1], criterion_result[2])
        elif len(criterion_result) != 3:
            print(f"Error with rubric category {criterion}, split wrong")
        else:
            print(f"Error with rubric category {criterion}, second entry not a number")
    return (numerical_result, comment_result)

### OUTPUTTING RESULTS ###
#helper function to format result

if __name__ == "__main__":
   result = grade()
   print(result[0])
 
