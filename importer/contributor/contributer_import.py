import pandas as pd
import pickle
from tqdm import tqdm

from importer.contributor.helper.github import response_generator
from settings import end_date


def get_user_num_commits_role(username: str, project: str):
    url = f"https://api.github.com/repos/{project}/commits?committer={username}&until={end_date}"
    return len(list(response_generator(url)))


def get_user_num_issues_role(username: str, project: str):
    url = f"https://api.github.com/repos/{project}/issues?creator={username}&until={end_date}"
    return len(list(response_generator(url)))


def run():
    projects = {}

    df = pd.read_pickle("analysis/processed_df.p")

    project_name: str
    reporter: str
    discussants: list[str]
    cnt = 0

    for project_name, reporter, discussants in tqdm(
        zip(df["project"], df["reporter"], df["discussants"]), desc="Issues"
    ):
        if project_name not in projects:
            projects[project_name] = {}

        for username in discussants + [reporter]:
            if username not in projects[project_name]:
                projects[project_name][username] = {
                    "commits": get_user_num_commits_role(username, project_name),
                    "issues": get_user_num_issues_role(username, project_name),
                }

        cnt += 1

        if cnt % 500 == 0:
            print("... saving current data")
            pickle.dump(projects, open("projects.p", "wb"))

    pickle.dump(projects, open("projects.p", "wb"))
