from tqdm import tqdm
import pickle
import itertools
from requests import Session
from datetime import datetime

from settings import api_search_url, api_header, adoption_gdpr, end_date, keywords
from importer.repository.helper.requests import get_from_pages, get_session, search
from importer.repository.helper.repository import is_development_active, is_issue_active


repository_cache = {}


def repository_requirements(session: Session, repository_url: str) -> bool:
    '''
    Checks if the repository meets the papers requirements. Uses cache to in an attempt to reduce the number of api requests.

        • public projects that are not forks and contain a license agreement;
        • at least ten contributors after June 20182;
        • active development with at least 100 commits after June 2018;
        • active usage of GitHub issues with at least 20 issues reported after June 2018;
    '''
    global repository_cache

    if (repository_url in repository_cache):
        return repository_cache[repository_url]

    repository = session.get(repository_url, headers=api_header).json()

    try:
        requirements_fulfilled = \
            repository["private"] == False and\
            repository["fork"] == False and\
            repository["license"] != None and\
            is_issue_active(repository_url) and\
            is_development_active(repository_url)
    except:
        print(repository)
        return False

    repository_cache[repository_url] = requirements_fulfilled

    return requirements_fulfilled


def run():
    global repository_cache

    session = get_session()

    for keyword in tqdm(keywords, position=2, desc="keyword"):
        issues = []
        for page in tqdm(search(api_search_url, keyword, adoption_gdpr, end_date), position=1, desc="pages"):
            for search_result in tqdm(page['items'], position=0, desc="results"):
                if (repository_requirements(session, search_result['repository_url'])):
                    '''
                    required variables: 
                        reporter                issue -> user
                        discussants             comments
                        labels                  issue -> labels
                        #comments               issue -> comments
                        #discussants            comments
                        reporting_date          issue -> created_at
                        last_active_date        issue -> updated_at
                        status                  issue -> state
                        privacy_issue
                        consent_interaction
                        resolution              comments

                    other things to store:
                        issue url
                    '''

                    issue = session.get(
                        search_result['url'], headers=api_header).json()
                    comments = list(itertools.chain.from_iterable(get_from_pages(
                        issue['comments_url'], {'per_page': 100}, headers=api_header)))

                    issues.append({
                        'url': issue['url'],
                        'created_at': datetime.fromisoformat(issue['created_at'][0:-1]),
                        'title': issue['title'],
                        'issue': issue,
                        'comments': comments
                    })

        pickle.dump(issues, open(f'issues_{keyword}.p', 'wb'))
