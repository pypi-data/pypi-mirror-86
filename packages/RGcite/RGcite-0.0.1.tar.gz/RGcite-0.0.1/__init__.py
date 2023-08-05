import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


faculty = ["Shilpa_Sonawani", "Mangesh_Bedekar"]

def find_articles(i):
    url = "https://www.researchgate.net/profile/" + i
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    names = []
    title = []

    for div in soup.findAll('a', {'class': 'nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare'}):
        names.append(div.text.strip())

    for name in names:
        p = name.split()
        if len(p) > 3:
            title.append(name)

    return title


def find_article_links(i):
    url = "https://www.researchgate.net/profile/" + i
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    links = []

    for div in soup.findAll('a', {
        'class': 'nova-c-button nova-c-button--align-center nova-c-button--radius-m nova-c-button--size-s '
                 'nova-c-button--color-blue nova-c-button--theme-bare nova-c-button--width-auto '
                 'nova-v-publication-item__action'}):
        links.append(div.get('href', None))

    return links


def find_citation(i):
    url = "https://www.researchgate.net/profile/" + i
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    citation_count = []

    for div in soup.findAll('div', {
        'class': 'nova-e-text nova-e-text--size-xl nova-e-text--family-sans-serif nova-e-text--spacing-none '
                 'nova-e-text--color-inherit'}):
        citation_count.append(div.text.strip())

    return citation_count[2]
