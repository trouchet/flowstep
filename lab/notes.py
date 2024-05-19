from json import load
import pandas as pd

with open('TODO.json') as f:
    data = load(f)

set(map(lambda x: x['level'], data['tasks']))

tasks = {
    'title': [],
    'description': [],
    'level': [],
    'level_description': [],
}

difficulty_level = {
    'Easy': 1,
    'Easy-Medium': 2,
    'Medium': 3,
    'Medium-Hard': 4,
    'Hard': 5,
}

for task in data['tasks']:
    tasks['title'].append(task['title'])
    tasks['description'].append(task['description'])

    level_description = task['level']
    tasks['level_description'].append(level_description)
    tasks['level'].append(difficulty_level[level_description])

tasks_df = pd.DataFrame(tasks)

tasks_df.sort_values(by='level', inplace=True)
tasks_df.reset_index(drop=True, inplace=True)

tasks_df.to_csv('TODO.csv', index=False)
