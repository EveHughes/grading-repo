import openai
from pathlib import Path
import pandas as pd

CATEGORIES = ["Download", "Clean", "Comments", "Caption", "Figure", "Sentence", "Total"]

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

#reads in scripts into one string
def read_scripts():
    scripts = ""
    path = Path(__file__).parent / ("input/scripts")
    for file in path.iterdir():
        if file.is_file():
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    scripts += file.name + "\n\n" + content
            except Exception as e:
                print(f"Error reading {file.name}: {e}")
    return scripts

#reads in tests into one string
def read_tests():
    tests = ""
    path = Path(__file__).parent / ("input/tests")
    for file in path.iterdir():
        if file.is_file():
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    tests += file.name + "\n\n" + content
            except Exception as e:
                print(f"Error reading {file.name}: {e}")
    return tests

#reads in paper into one string
def read_paper():
    file_path = Path(__file__).parent / ("input/paper.qmd")
    with open(file_path, "r", encoding="utf-8") as f:
        paper = f.read()
    return paper

#reads in project to dictionary -- seperates scripts, tests & paper
def read_project():
    project = {}
    project["Scripts"] = read_scripts()
    project["Tests"] = read_tests()
    project["Paper"] = read_paper()
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

#goes through entire rubric and grades
def grade():
    #reads in the files
    rubric = read_rubric()
    prompt = read_prompt(1)
    project = read_project()

    numerical_result = {}
    comment_result = {}
    #calls the grader
    for criterion in rubric:
        if criterion not in ["reproducible.txt", "tests.txt"]:
            criterion_result = grade_criterion(project["Paper"], rubric[criterion], prompt)
        elif criterion not in ["tests.txt"]:
            print("here in reproducible")
            criterion_result = grade_criterion(project["Scripts"], rubric[criterion], prompt)
        else:
            print("here in tests")
            criterion_result = grade_criterion(project["Tests"], rubric[criterion], prompt)

        criterion_result = criterion_result.split(";")

        #prints the grade and comment, or prints an error message
        if len(criterion_result) == 3 and criterion_result[1].isnumeric():
            numerical_result[criterion_result[0]] = criterion_result[1]
            comment_result[criterion_result[0]] = criterion_result[2]
            print(criterion_result)
        elif len(criterion_result) != 3:
            print(f"Error with rubric category {criterion}, split wrong")
        else:
            print(f"Error with rubric category {criterion}, second entry not a number")
    
    return (numerical_result, comment_result)

### OUTPUTTING RESULTS ###
#helper function to format result

if __name__ == "__main__":
   result = grade()
   #prints the numerical results
   print(result[0])
 
