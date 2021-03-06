Aristotle is a highly customizable tool that collects links from sites.

![Aristotle](aristotle.png)

With the properties in the config files, it scans all the defined sites and saves the metadata [title, description, imageLink, publishDate] of the site in the database.

## Usage

#### config/properties.yaml

These settings are basically:

1. **database:** Currently, databases in this list ((https://docs.sqlalchemy.org/en/13/dialects/)) are supported. The settings of the DB where the links will be stored are entered here. For the `name` property, a database must be created in the DB and its name must be entered in this parameter.
2. **locale:** According to the language of the sites to be fetched, the feature to be localized must be entered here. For example, in English, en_EN should be entered.
3. **request:** General features of the request.
4. **parser:** In the parsing phase, if desired, title and description strings can be trimmed as much as the parameter given

```yaml
database:
  dialect: mysql+pymysql
  url: localhost
  port: 3306
  name: aristotle
  userName: root
  password: root

locale: en_EN

request:
  timeout: 3
  userAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML) Chrome/23.0.1271.97 Safari/537.11

parser:
  titleCharLimit: 100
  descriptionCharLimit: 300
```

#### config/sources-{locale}.yaml
```yaml
article:
  - domain: cnn.com
    active: true
    link: https://edition.cnn.com/
    filterForLink:
      mandatoryWords: ["/politics/"]
      permissibleWords: []
      impermissibleWords: []
    tagForMetadata:
      title:
      description:
      image:
      publishDate:
      publishDateFormat: "%Y-%m-%d"

technology:
  - domain: mashable.com
    active: true
    link: https://mashable.com
    filterForLink:
      mandatoryWords: ["-"]
      permissibleWords: ['/article/']
      impermissibleWords: []
    tagForMetadata:
      title:
      description:
      image:
      publishDate: datetime
      publishDateFormat: "%d.%m.%Y"

```


## Development
If you'd like to contribute the project, feel free to clone a development version of this repository locally:

`git clone https://github.com/egcodes/aristotle.git`

Once you have a copy of the source, you can embed it in your Python package, or install it into your site-packages easily:

```
$ pip3 install -r requirements.txt
$ python3 setup.py install
```
### Requirements

- Python 3.x 
	- beautifulsoup4>=4.9.1
    - requests>=2.24.0
    - PyYAML>=5.3.1
    - SQLAlchemy>=1.3.18
    
For database dialect, you must install the special dialect package for the database you use. 
For example, if you are using MySQL, the `PyMySQL` package must be installed.
