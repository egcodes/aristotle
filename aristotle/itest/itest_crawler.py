from crawler import Crawler

crawler = Crawler(
"technology",
"mashable.com",
"https://mashable.com/article/elon-musk-aliens-pyramids-conspiracy-theory/"
)
crawler.run()

print(crawler.getTitle())
print(crawler.getDescription())
print(crawler.getImage())
print(crawler.getPublishDate())


