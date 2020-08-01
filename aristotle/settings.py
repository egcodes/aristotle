import logging.config
import yaml
import locale


def getProps(*propertyList):
    property = ""
    for prop in propertyList:
        if not property:
            property = props.get(prop)
            continue
        property = property.get(prop)
    return property


def getDomainProps(domain, *propertyList):
    for category in sources:
        for domainProp in sources.get(category):
            if domainProp.get("domain") == domain:
                if propertyList:
                    property = ""
                    for prop in propertyList:
                        if not property:
                            property = domainProp.get(prop)
                            continue
                        property = property.get(prop)
                    return property
                else:
                    return domainProp


with open(r'config/properties.yaml') as file:
    props = yaml.load(file, Loader=yaml.FullLoader)

loc = props.get("locale")

with open(r'config/sources-%s.yaml'%getProps("locale")) as file:
    sources = yaml.load(file, Loader=yaml.FullLoader)

locale.setlocale(locale.LC_ALL, loc)

logging.config.dictConfig(yaml.load(open('config/logging.yaml', 'r'), Loader=yaml.FullLoader))
