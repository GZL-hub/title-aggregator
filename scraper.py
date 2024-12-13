import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse as date_parse

# URL of the website to scrape
URL = 'https://mashable.com/'

# Send a GET request to the website
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all article links
articles = soup.find_all('a', class_='block mt-2 w-full text-lg font-semibold leading-tight')
print(f"Scraped {len(articles)} articles.")

# Collect headlines, hyperlinks, and publication dates
collected_articles = []
for article in articles:
    title = article.get_text().strip()
    url = article['href']
    if not url.startswith('http'):
        url = 'https://mashable.com' + url
    
    # Fetch the article page to get the publication date
    article_response = requests.get(url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    # Find the publication date (assuming it's in a <time> tag with datetime attribute)
    date_tag = article_soup.find('time')
    if date_tag and 'datetime' in date_tag.attrs:
        date_str = date_tag['datetime']
        try:
            date = date_parse(date_str).replace(tzinfo=None)
            if date >= datetime(2022, 1, 1):
                collected_articles.append((date, title, url))
        except ValueError:
            print(f"Error parsing date: {date_str}")

print(f"Collected {len(collected_articles)} articles from January 1, 2022 onwards.")

# Sort articles anti-chronologically
collected_articles.sort(reverse=True, key=lambda x: x[0])

# Generate HTML content
html_content = '''
<!DOCTYPE html>
<html>
<head>
<title>Title Aggregator</title>
<style>
body { font-family: Arial, sans-serif; background-color: #fff; color: #000; }
a { text-decoration: none; color: #000; }
a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>Article Titles</h1>
<ul>
'''

for date, title, url in collected_articles:
    html_content += f'''
<li><a href="{url}" target="_blank">{title}</a> ({date.strftime("%Y-%m-%d")})</li>
'''

html_content += '''
</ul>
</body>
</html>
'''

# Ensure the templates directory exists
os.makedirs('templates', exist_ok=True)

# Write HTML content to templates/index.html
with open('templates/index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("Headlines have been saved to templates/index.html")