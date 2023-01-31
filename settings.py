private_token = "github_key"

api_search_url = 'https://api.github.com/search/issues'
api_header = {'accept': 'application/vnd.github+json', 'Authorization': f'Bearer {private_token}', 'X-GitHub-Api-Version': '2022-11-28'}

keywords = [
    "anonymization",
    "CCPA",
    "consent withdrawal",
    "cookie banner",
    "cookie law",
    "cookie notice",
    "cookie prompt",
    "data breach",
    "data privacy",
    "data protection",
    "data sharing",
    "ePrivacy Directive",
    "fingerprinting",
    "GDPR",
    "personal data",
    "personally identifiable information",
    "PII",
    "privacy act",
    "privacy breach",
    "privacy controls",
    "privacy issue",
    "privacy law",
    "privacy notice",
    "privacy policy",
    "privacy problem",
    "privacy settings",
    "privacy violation",
    "pseudonymization",
    "right to be forgotten",
    "tracking"
]

adoption_gdpr = "2016-04-01T00:00:00"
enforcable_gdpr = "2018-06-01T23:59:59"
end_date = "2022-12-31T23:59:59"

min_contributers = 10
min_commits = 100
min_issues = 20