from nicegui import ui
import polars as pl

import sys
sys.dont_write_bytecode = True

from pathlib import Path
base_path = Path(__file__).resolve().parent.parent
sys.path.insert(1, str(base_path / 'api_interaction'))
sys.path.insert(1, str(base_path / 'file_formatting'))

from grading import *
from download import *

def grader(task, rubric, repo_link):
    ui.notify('Calculating grade')
    # download(repo_link)
    # save_task(task)
    # save_rubric(rubric)
    # grade()

    path = Path(__file__).resolve().parent.parent
    df = pl.read_csv(path / "api_interaction/output/response.csv")
    ui.table.from_polars(df).classes('max-h-40')    

ui.label("autograder")
task = ui.textarea(label = 'Task', placeholder ='Enter the task')
rubric = ui.textarea(label='Rubric', placeholder='Enter your rubric')
repo_link = ui.input(label='Repo', placeholder='Enter your github repo')
button = ui.button('Calculate Grade', on_click=lambda: grader(task.value, rubric.value, repo_link.value))

ui.run()