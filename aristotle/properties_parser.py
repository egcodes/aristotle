from util import *


def getTitle(domainProps, soup):
    title = soup.find(domainProps["title"]).text
    if title:
        return title
    else:
        return ""


def getDescription(domainProps, soup):
    description = soup.find(domainProps["description"]).text
    if description:
        return description
    else:
        return ""


def getImage(domainProps, soup):
    image = soup.find(domainProps["image"])
    if image:
        return image
    else:
        return ""


def getPublishDate(domainProps, soup):
    publishDate = ""
    tags = domainProps["publishDate"].split(",")
    if len(tags) == 3:  # <div class="date">01.08.2020 18:17</div>
        publishDate = soup.find(tags[0], {tags[1]: tags[2]})
    elif len(tags) == 2:  # <time datetime="2020-08-01T18:26:08+03:00"></time>
        part = soup.find(tags[0])
        if part:
            try:
                publishDate = part[tags[1]]
            except:
                pass
    if publishDate:
        if type(publishDate) != str:
            publishDate = publishDate.text
        return trim_str(publishDate, 100)
    return ""
