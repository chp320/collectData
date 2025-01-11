import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def search_naver_blog_posts(query, days_within=7, num_results=10):
  headers = {'User-Agent': 'Mozilla/5.0'}
  search_url = f"https://search.naver.com/search.naver?where=post&query={query}"
  print(f"Search URL: {search_url}")  # 검색 URL 확인
  response = requests.get(search_url, headers=headers)
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'html.parser')

  posts = []
  today = datetime.now()
  date_limit = timedelta(days=days_within)
  print(f"Date limit: {date_limit}")  # 날짜 제한 확인

  for item in soup.find_all('li', class_='sh_blog_top'):
    # 제목과 링크 추출
    title_tag = item.find('a', class_='title_link')
    if title_tag:
      title = title_tag.get('title')
      url = title_tag.get('href')
      print(f"Found post: {title}, URL: {url}")   # 발견한 게시글 정보 출력

    print(f"before date_tag.")
    # 날짜 추출
    date_tag = item.find('dd', class_='txt_inline')
    if date_tag:
      date_str = date_tag.get_text()
      print(f"Parsed post date: {post_date}") # 파싱된 날짜 출력
      try:
        # 날짜 형식 파싱 (ex. '2025.01.11')
        post_date = datetime.strptime(date_str, '%Y.%m.%d')
        print(f"Post added: {post_date}") # 파싱된 날짜 출력

        # 날짜 비교 ( 지정된 날짜이내 데이터만 추출하기 위함 )
        if date_limit <= post_date <= today:
          posts.append((title, url, post_date))
          print(f"Post added: {title}") # 추가된 게시글 정보 출력
      except ValueError:
        # 날짜 형식이 맞지 않는 경우
        print(f"Date parsing failed for : {date_str}")  # 날짜 파싱 실패 시 출력
        continue
    print(f"after date_tag.")

    # 원하는 수의 결과만 수집
    if len(posts) >= num_results:
      print(f"Reached the desired number of results.")
      break

  print(f"done.")

  return posts

query = "서평단 모집"
posts = search_naver_blog_posts(query)
for title, url, post_date in posts:
  print(f"Title: {title}\nURL: {url}\nDate: {post_date.strftime('%Y-%m-%d')}\n")

