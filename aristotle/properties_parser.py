def getTitle(domainProps, soup):
    return soup.find(domainProps["title"]).text


def getDescription(domainProps, soup):
    return soup.find(domainProps["description"]).text


def getImage(domainProps, soup):
    return soup.find(domainProps["image"]).text


def getPublishDate(domainProps, soup):
    tags = domainProps["publishDate"].split(",")
    if len(tags) == 3: # <div class="date">01.08.2020 18:17</div>
        publishDate = soup.find(tags[0], {tags[1]: tags[2]})
        if publishDate:
            publishDate = publishDate.text
    elif len(tags) == 2: # <time datetime="2020-08-01T18:26:08+03:00"></time>
        publishDate = soup.find(tags[0])[tags[1]]

    return publishDate

