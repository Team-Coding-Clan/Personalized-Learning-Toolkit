from urllib.parse import urlparse
import requests

URL = "https://api.github.com/"


def get_skills(github_profile):
    # https: // api.github.com / repos / Shikha291 /${name} / languages
    # 'https://www.github.com/tawishisharma/'
    data = urlparse(github_profile)
    owner = data.path
    # print(owner)
    # print(owner.path)
    # get public repositories from user github profile
    repos_url = URL + "users" + owner + "repos"
    # print(repos_url)
    response = requests.get(repos_url)
    repos_data = response.json()  # over fetching
    languages = []
    for repo in repos_data:
        repo_name = repo['name']
        # print(repo_name)
        lang_url = URL + "repos" + owner + repo_name + "/languages"
        # print(lang_url)
        response = requests.get(lang_url)
        language = response.json()
        # print(language)
        languages.append(language)

    print(languages)
    # put into database
    return languages
