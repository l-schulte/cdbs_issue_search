from settings import enforcable_gdpr, end_date, min_contributers, min_commits, min_issues
from importer.helper.requests import get_from_pages


def is_development_active(repository_url: str):
    '''Returns True if the #authors and #commits between the effective date of GDPR and end date of the study excede the minimum requirement'''
    authors = {}
    commit_count = 0
    for page in get_from_pages(repository_url + '/commits', {'since': enforcable_gdpr, 'until': end_date, 'per_page': 100}):
        commit_count += len(page)
        for commit in page:
            authors[commit['commit']['author']['name']] = True
            if (len(authors.keys()) >= min_contributers and commit_count >= min_commits):
                return True

    return False


def is_issue_active(repository_url: str):
    '''Returns true if the #issues between the effective date of GDPR and the end date of the study excedes the minimum requirement'''
    issue_count = 0
    for page in get_from_pages(repository_url + '/issues', {'since': enforcable_gdpr, 'until': end_date, 'per_page': min_issues}):
        issue_count += len(page)
        if (issue_count >= min_issues):
            return True

    return False
