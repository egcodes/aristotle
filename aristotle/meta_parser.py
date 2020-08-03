from settings import getProps


def getTitle(metas):
    attrs = getProps("parser", "metaTitle")
    for meta in metas:
        if 'name' in meta.attrs:
            if meta.attrs['name'] in attrs:
                return getMetaText(meta)

        elif 'property' in meta.attrs:
            if meta.attrs['property'] in attrs:
                title = getMetaText(meta)
                if title:
                    return title
    return ""


def getDescription(metas):
    attrs = getProps("parser", "metaDescription")
    for meta in metas:
        if 'name' in meta.attrs:
            if meta.attrs['name'] in attrs:
                return getMetaText(meta)

        elif 'property' in meta.attrs:
            if meta.attrs['property'] in attrs:
                desc = getMetaText(meta)
                if desc:
                    return desc
    return ""


def getImage(metas):
    attrs = getProps("parser", "metaImage")
    for meta in metas:
        if 'property' in meta.attrs:
            if meta.attrs['property'] in attrs:
                image = getMetaText(meta)
                if image:
                    return image
    return ""


def getPublishDate(metas):
    attrs = getProps("parser", "metaPublishDate")
    for meta in metas:
        if 'property' in meta.attrs:
            if meta.attrs['property'] in attrs:
                return getMetaText(meta)

        elif 'itemprop' in meta.attrs:
            if meta.attrs['itemprop'] in attrs:
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
