import openai
from pathlib import Path
import polars as pl
from datetime import datetime


### READING IN FILES ###
#get key
with open('key.txt', 'r') as file:
    my_key = file.read().strip()

#reading in prompt based on number specified
def read_prompt(i):
    file_path = Path(__file__).parent / ("prompts/prompt" + str(i) + ".txt")
    with open(file_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()
    return prompt_text

#reads in rubric as a dictionary, file name -> file content
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

#reads in all scripts into one string
def read_scripts(project_name):
    scripts = ""
    path = Path(__file__).parent.parent / (f"benchmark_repos/{project_name}/scripts")
    for file in path.iterdir():
        if file.is_file():
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    scripts += file.name + "\n\n" + content
            except Exception as e:
                print(f"Error reading {file.name}: {e}")
    return scripts

#reads in paper into one string
def read_paper(project_name):
    file_path = Path(__file__).parent.parent / (f"benchmark_repos/{project_name}/paper/paper.qmd")
    with open(file_path, "r", encoding="utf-8") as f:
        paper = f.read()
    return paper

#reads in project to dictionary -- seperates scripts, & paper.qmd, and paper.pdf
def read_project(project_name):
    project = {}
    project["Scripts"] = read_scripts(project_name)
    project["Paper"] = read_paper(project_name)
    return project

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


### OUTPUTTING RESULTS ###
#outputs result into csv
def to_response_csv(numerical_result, comment_result):
    dic = {"criterion": [], "grade": [], "comment": []}
    for criterion in numerical_result:
        dic["criterion"].append(criterion)
        dic["grade"].append(numerical_result[criterion])
        dic["comment"].append(comment_result[criterion])
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
    

## AUTOGRADING ##
#goes through entire rubric and grades
def grade(project_name):
    #reads in the files
    rubric = read_rubric()
    prompt = read_prompt(1)
    project = read_project(project_name)

    numerical_result = {}
    comment_result = {}

    #calls the grader
    for criterion in rubric:
        while True:
            if criterion not in ["reproducible.txt", "tests.txt"]:
                criterion_result = grade_criterion(project["Paper"], rubric[criterion], prompt)
            else: 
                criterion_result = grade_criterion(project["Scripts"], rubric[criterion], prompt)

            criterion_result = criterion_result.split(";")

            #prints the grade and comment, or prints an error message
            if len(criterion_result) == 3 and criterion_result[1].isnumeric():
                numerical_result[criterion] = criterion_result[1]
                comment_result[criterion] = criterion_result[2]
                print(criterion_result)
                break
            elif len(criterion_result) != 3:
                print(f"Error with rubric category {criterion}, split wrong")
            else:
                print(f"Error with rubric category {criterion}, second entry not a number")
    
    #updates the csvs
    to_response_csv(numerical_result, comment_result)
    update_history_csv(numerical_result)
    return (numerical_result, comment_result)


if __name__ == "__main__":
   result = grade("project1")
   #prints the numerical results
   print(result[0])