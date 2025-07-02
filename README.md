# Donaldson Project Autograder
# ==========================
## Overview
The Donaldson Project Autograder is a Python-based tool designed to automatically generate and evaluate 'Donaldson projects' based on a rubric. A Donaldson project consists of downloading data from Open Data Toronto, cleaning the data, testing it, and writing a paper using Quarto expressing findings. The autograder utlizes LLMs (Large Language Model) as a judge as well as a set of deterministic checks to evaluate the projects.

## Repository Structure
The repository is structured as follows:

```
grading-repo/
├── benchmark_repos/            # Folder containing benchmark projects for testing
├── paper_generation/           
│   ├── prompt/                 # Prompts used to generate project
│   └── create.py               # Pythom script to generate project from prompts
├── paper_grading/             
│   ├── prompts/                # Stores prompt files for grading
│   ├── rubric/                 # Contains one txt file per rubric category
│   └── grading.py              # Grading script to evaluate gprojects
└──result/                     
    ├── history.csv             # Log of past grading results
    └── responses/               # Responses generated from autograder
```