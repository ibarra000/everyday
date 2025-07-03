#!/usr/bin/env python3

from ollama import chat
import glob
import sys
import day1

day1.greet()

past_projects_files = glob.glob("./*.txt")
past_projects = ""
for project_file in past_projects_files:
    with open(project_file, "r") as file:
        past_projects += "* " + file.read().strip() + "\n"
print("Past Projects:\n")
print(past_projects)
day1.print_full_width_line()
todays_request = input("What kind of project are we feeling today?\n")

stream = chat(
        model='llama3.2',
        messages=[{'role':'user', 'content':f'Omit the Preamble. Do not explicitly code. Any code generated should be esoteric or pseudo code. Now, suggest a simple python coding projects that covers this request: {todays_request}. It must also build off the following projects: {past_projects}.'}],
        stream=True,
        )
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
