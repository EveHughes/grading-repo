#### Preamble ####
# Purpose: Download and process files necessary for grading Donaldson Project.
# Author: Evelyn Hughes
# Date: 04 July 2025
# Contact: evelyn.hughes@utoronto.ca
# Pre-requisites: None

from pathlib import Path

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