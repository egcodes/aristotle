def getTitle(metas):
    for meta in metas:
        if 'name' in meta.attrs:
            metaName = meta.attrs['name']
            if metaName in "title":
                return getMetaText(meta)

        elif 'property' in meta.attrs:
            metaProperty = meta.attrs['property']
            if metaProperty in "og:title":
                return getMetaText(meta)
    return ""


def getDescription(metas):
    for meta in metas:
        if 'name' in meta.attrs:
            metaName = meta.attrs['name']
            if metaName in ["description", "og:description"]:
                return getMetaText(meta)

        elif 'property' in meta.attrs:
            metaProperty = meta.attrs['property']
            if metaProperty in "og:description":
                return getMetaText(meta)
    return ""


def getImage(metas):
    for meta in metas:
        if 'property' in meta.attrs:
            metaProperty = meta.attrs['property']
            if metaProperty in ["og:image", "og:image:url"]:
                return getMetaText(meta)
    return ""


def getPublishDate(metas):
    for meta in metas:
        if 'property' in meta.attrs:
            metaProperty = meta.attrs['property']
            if metaProperty in ["datePublished", "og:article:published_time", "article:published_time"]:
                return getMetaText(meta)

        elif 'itemprop' in meta.attrs:
            metaItemprop = meta.attrs['itemprop']
            if metaItemprop in "datePublished":
                return getMetaText(meta)
    return ""


def getMetaText(meta):
    try:
        return meta.attrs["content"]
    except:
        try:
            return meta.attrs["value"]
        except:
            return ""
