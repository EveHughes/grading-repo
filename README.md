# Donaldson Project Autograder
# ==========================
## Overview
The Donaldson Project Autograder is a Python-based tool designed to automatically generate and evaluate 'Donaldson projects' based on a rubric. A Donaldson project consists of downloading data from Open Data Toronto, cleaning the data, testing it, and writing a paper using Quarto expressing findings. The autograder utlizes LLMs (Large Language Model) as a judge to evaluate the projects.

## Repository Structure
The repository is structured as follows:

```
grading-repo/
├── benchmark_repos/            # Folder containing benchmark projects for testing
├── paper_generation/           
│   ├── prompt/                 # Prompts used to generate project
│   └── create.py               # Python script to generate project from prompts
├── paper_grading/             
│   ├── prompts/                # Stores prompt files for grading
│   ├── rubric/ 
│   ├── grading_all.py          # Main script for evaluating projects -- grades multiple criterion at a time
│   ├── grading.py              # Main script for evaluating projects -- grades one criterion at a time
│   ├── read.py                 # Functions to read in inputs for grading
│   └── write.py                # Functions to process LLM grading output to csv
└──result/                     
    ├── history.csv             # Log of past grading results
    └── responses/              # Responses generated from autograder
```