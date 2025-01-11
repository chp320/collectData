import requests
from bs4 import BeautifulSoup

def search_urls(query, num_results=10): 
  headers = {'User-Agent': 'Mozilla/5.0'}
  search_url = f"https://www.google.com/search?q={query}&num={num_results}"
  response = requests.get(search_url, headers=headers)
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'html.parser')
  links = []

  for item in soup.find_all('a'):
    href = item.get('href')
    if href and href.startswith('/url?q='):
      url = href.split('/url?q=')[1].split('&')[0]
      links.append(url)
  return links

query = "서평단 모집"
urls = search_urls(query)
for url in urls:
  print(url)

