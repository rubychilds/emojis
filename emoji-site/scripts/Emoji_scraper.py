from requests import get
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd

url = 'http://emojipedia.org'


def get_soup(url):
    r = get(url)
    return BeautifulSoup(r.text, 'html.parser')


def get_main_categories():
    soup = get_soup(url)
    catgeories_with_ref = defaultdict(str)
    for div in soup.findAll('div'):
        if 'block' in div.attrs.get('class', []) and div.h2 and \
                div.h2.text == 'Categories':
            for page in div.findAll('li'):
                category_url_ref = page.find('a').get('href')
                category = page.find('a').text
                if 'http://' not in category_url_ref:
                    catgeories_with_ref[category_url_ref] = category
    return catgeories_with_ref


def get_category_with_urls(categories_with_ref):
    cat_with_urls = defaultdict(list)
    for url_ext, cat in list(categories_with_ref.items()):
        mini_soup = get_soup(url + url_ext)
        divs = mini_soup.findAll('div')
        clean_cat = ' '.join(cat.split()[1:])
        for div in divs:
            if div.h1:
                name = ' '.join(div.h1.text.strip().split()[1:])
                if name in clean_cat:
                    for l in div.findAll('li'):
                        if 'http://' not in l.find('a').get('href'):
                            cat_with_urls[cat] += [l.find('a').get('href')]
    return cat_with_urls


def extract_emoji_info(url):
    soup = get_soup(url)
    # TITLE
    title = soup.h1.text
    # DESCRIPTION
    sections = soup.findAll('section')
    aliases = []
    description = ''
    for section in sections:
        name = section.get('class')[0]
        if name == 'description':
            description = section.p.text
        if name == 'aliases':

            for alias_item in sections[1].findAll('li'):
                aliases.append(' '.join(alias_item.text.split()[1:]))

    shortcodes = []
    for l in soup.findAll('ul'):
        if l.get('class', [''])[0] == 'shortcodes':
            shortcodes = [shortcode_nest.text for shortcode_nest in l.findAll('li')]

    return {'name': title if title else ' '.join(title.split()[1:]),
            'clean_name': ' '.join(title.split()[1:]),
            'description': description,
            'alternate_names': aliases,
            'shortcodes': shortcodes,
            'url': url
            }


def extract_all_page_info(cat_with_urls):
    data = []
    for cat, urls in list(cat_with_urls.items()):
        for url_ext in list(set(urls)):
            extracted = extract_emoji_info(url + url_ext)
            if extracted.get('name') != '':
                data.append(extracted)
    data = pd.DataFrame(data)
    data.to_csv('data/emoji_lookup.csv')
    return data


def main():
    categories_with_ref = get_main_categories()
    cat_with_urls = get_category_with_urls(categories_with_ref)
    extract_all_page_info(cat_with_urls)


if __name__ == '__main__':
    main()
