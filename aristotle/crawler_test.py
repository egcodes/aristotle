from crawler import Crawler

crawler = Crawler(
"technology",
"mashable.com",
"https://mashable.com/article/best-80s-movies-on-netflix/"
)
crawler.run()

print(crawler.getTitle())
print(crawler.getDescription())
print(crawler.getImage())
print(crawler.getPublishDate())