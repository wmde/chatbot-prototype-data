import json
import requests
from bs4 import BeautifulSoup

wikipedia_api_url = 'https://de.wikipedia.org/w/api.php'
article_source_category = 'Kategorie:Wikipedia:Exzellent'

def list_articles_in_category(category):
    articles = []

    should_fetch_next_batch = True
    continuation_token = ''

    while should_fetch_next_batch:
        response = requests.get(
                wikipedia_api_url,
                params={
                    'action': 'query',
                    'list': 'categorymembers',
                    'cmtitle': category,
                    'cmnamespace':  0,
                    'cmlimit': 500,
                    'cmcontinue': continuation_token,
                    'format': 'json',
                }
        ).json()

        should_fetch_next_batch = 'continue' in response
        if should_fetch_next_batch:
            continuation_token = response['continue']['cmcontinue']

        for member in response['query']['categorymembers']:
            articles.append(member['title'])

    return articles

def get_url_of_article(article_title):
    response = requests.get(
            wikipedia_api_url,
            params={
                'action': 'query',
                'titles': article_title,
                'prop': 'info',
                'inprop': 'url',
                'format': 'json',
            }
    ).json()

    page_info = list(response['query']['pages'].values())[0]
    return page_info['fullurl']

def get_text_from_article(article_title):
    response = requests.get(
            wikipedia_api_url,
            params={
                'action': 'parse',
                'page': article_title,
                'prop': 'text',
                'format': 'json',
            }
    ).json()

    page_html = response['parse']['text']['*']

    parsed_html = BeautifulSoup(page_html, 'lxml')

    return parsed_html.get_text()

def main():
    result = {}

    articles = list_articles_in_category(article_source_category)

    for article in articles:
        article_url = get_url_of_article(article)
        article_text = get_text_from_article(article)

        result[article_url] = article_text

    print(json.dumps(result))

if __name__ == '__main__':
    main()
