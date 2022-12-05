from urllib.parse import urlparse
import requests
from pprint import pprint
from celery import shared_task
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

GITHUB_URL = "https://api.github.com/"
headers = {
    'Authorization': 'token TOKEN',
}
KEY = 'AIzaSyA78Bfr50t93zRCpnypkxEUulcpGFdgIA0'
GOOGLE_BOOKS_KEY = 'AIzaSyA78Bfr50t93zRCpnypkxEUulcpGFdgIA0'


@shared_task
def rate_limit_check():
    response = requests.get('https://api.github.com/rate_limit')
    remaining_requests = response.json()['resources']['core']['remaining']
    return remaining_requests > 0


@shared_task
def get_skills(github_profile):
    # https: // api.github.com / repos / Shikha291 /${name} / languages
    # 'https://www.github.com/tawishisharma/'
    data = urlparse(github_profile)
    owner = data.path
    # get public repositories from user github profile
    repos_url = GITHUB_URL + "users" + owner + "repos"
    response = requests.get(repos_url)
    repos_data = response.json()  # over fetching
    languages = set()

    # todo: error handling for when rate limit exceeds in Github API
    # problem: we are using a for loop and so we get rate limited when
    # we do this for more than 60 repositories in a minute
    # it takes approximately one hour to reset the limit to 60
    '''For unauthenticated requests, the rate limit allows for up to 60 requests per hour. Unauthenticated requests are
     associated with the originating IP address, and not the person making requests.
     The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret, 
     you can make up to 30 requests per minute. For unauthenticated requests, the rate limit allows you to make up to 
     10 requests per minute.
     '''

    for repo in repos_data:
        if not rate_limit_check():
            return []
        repo_name = repo['name']
        lang_url = GITHUB_URL + "repos" + owner + repo_name + "/languages"
        response = requests.get(lang_url)
        repo_languages = list(response.json())
        # print(repo_languages)  # todo : remove no. of bytes from the request data
        for repo_language in repo_languages:
            languages.add(repo_language)

    languages = list(languages)
    # put into database
    # print("get_skills")
    return languages


# image link, url, title, description, source

@shared_task
def youtube_api(search_key):
    """
    Returns a list of max 20 videos per search_key
    """
    search_key = search_key + " courses"
    params = {'key': KEY, 'type': 'video', 'part': 'snippet', 'q': search_key, 'maxResults': 20}
    response = requests.get('https://www.googleapis.com/youtube/v3/search', params = params)
    # in response, we need the video id
    # response > items > iterate over list items > id > videdId
    # use this video id in YouTube url

    videos = []

    # get the videoId and hence the video of top 20 suggestions
    # the general youTube url : https://www.youtube.com/watch?v=id
    for video in response.json()['items']:
        video_id = video['id']['videoId']
        video_url = 'https://www.youtube.com/watch?v=' + video_id
        video_thumbnail_url = video['snippet']['thumbnails']['high']['url']
        video_title = video['snippet']['title']
        video_description = video['snippet']['description']
        # JSON object append to list
        videos.append({
            'url': video_url,
            'image': video_thumbnail_url,
            'title': video_title,
            'description': video_description
        }
        )
    # print("youtube")
    return videos


@shared_task
def google_books_api(search_key):
    """
       Returns a list of max 20 books per search_key
    """
    params = {'key': GOOGLE_BOOKS_KEY, 'q': search_key, 'maxResults': 20}

    response = requests.get('https://www.googleapis.com/books/v1/volumes', params = params)
    # in response, we need the url
    # response > items > iterate over list items > id

    books = []

    # get the url and hence the books of top 20 suggestions
    # the general youTube url : https://www.google.co.in/books/edition/
    for book in response.json()['items']:
        book_url = book['volumeInfo']['infoLink'] if 'infoLink' in book['volumeInfo'] else ''
        book_title = book['volumeInfo']['title'] if 'title' in book['volumeInfo'] else ''
        book_image = book['volumeInfo']['imageLinks']['thumbnail'] + '&zoom=0' if 'imageLinks' in book[
            'volumeInfo'] else ''
        book_description = book['volumeInfo']['description'] if 'description' in book['volumeInfo'] else ''
        # JSON object append to list
        books.append({
            'url': book_url,
            'image': book_image,
            'title': book_title,
            'description': book_description
        }
        )
    # print("google_books")
    return books


@shared_task
def coursera(search_key):
    path = 'C://chromedriver.exe'

    driver = webdriver.Chrome(executable_path = path)

    language = search_key
    driver.get("https://in.coursera.org/search?query={}&".format(language))

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    courses = []
    courses_selector = soup.find_all('li', class_ = 'cds-71 css-0 cds-73 cds-grid-item cds-118 cds-126 cds-138')

    # print(courses_selector)

    for course_selector in courses_selector:
        course_div = course_selector.find('div', class_ = 'css-1pa69gt')
        if course_div is None:
            continue
        course_div_title = course_div.find('div', class_ = 'css-1rj417c').find('h2').get_text()
        course_title = course_div_title.strip()
        course_div_img = course_div.find('div', class_ = 'css-1doy6bd').find('img')
        course_img = course_div_img['src']
        course_div_url = course_div.find('a')
        course_url = course_div_url['href']
        courses.append({'title': course_title, 'img': course_img, 'url': course_url})

    return courses