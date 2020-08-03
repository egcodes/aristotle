from bs4 import BeautifulSoup
from urllib.parse import urlparse

from settings import *
from util import *

log = logging.getLogger(__name__)


def get_filtered_links(htmlSource, category, domain):
    linkList = []
    soup = BeautifulSoup(htmlSource, 'html.parser')
    filterLinkProps = getDomainProps(category, domain, "filterForLink")

    def is_contain_mandatory_keywords():
        if filterLinkProps["mandatoryWords"]:
            for word in filterLinkProps["mandatoryWords"]:
                if word not in href:
                    return False
        return True

    def is_allowed():
        if filterLinkProps["permissibleWords"]:
            for word in filterLinkProps["permissibleWords"]:
                if word in href:
                    return True
            return False
        return True

    def is_forbidden():
        if filterLinkProps["impermissibleWords"]:
            for word in filterLinkProps["impermissibleWords"]:
                if word in href:
                    return True
        return False

    links = soup.findAll('a')
    log.info("Links count (page): %d", len(links))
    for link in links:
        try:
            href = link.attrs['href']
        except KeyError:
            continue

        parsed_uri = urlparse(href)
        if parsed_uri.netloc:
            if domain not in parsed_uri.netloc:
                continue

        if is_contain_mandatory_keywords() and is_allowed() and not is_forbidden():
            linkList.append(href)

    return linkList


def fix_broken_links(linkList, domain, link):
    for index, href in enumerate(linkList):
        parsed_uri = urlparse(href)
        if not parsed_uri.netloc:
            linkList[index] = "https://" + add_www(link) + domain + add_slash(href) + href
        elif href.startswith("//"):
            linkList[index] = "https://" + href[2:]

    return linkList
