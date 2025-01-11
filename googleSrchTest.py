#########################################################
# 구글 검색 결과 페이지 결과에서 링크 url 추출
#########################################################
import requests
from bs4 import BeautifulSoup

# 검색 키워드
search_query = "서평단+모집"

# 구글 검색 결과 페이지 url
base_url = f"https://www.google.com/search?q=intitle:%22{search_query}%22&as_qdr=m"

# GET 요청 보내기
response = requests.get(base_url)

# BeautifulSoup 으로 HTML 분석 - 아래에서 필요한 element 를 추출
soup = BeautifulSoup(response.text, 'html.parser')

# 연결된 링크 추출
links = []
# 모든 <a> 태그 중에서 href 속성을 가진 태그를 찾아 리스트로 저장
for a_tag in soup.find_all('a', href=True):
  href = a_tag['href']
  if href.startswith('/url?q='):
    real_link = href.split('/url?q=')[1].split('&')[0]
    links.append(real_link)

# 중복 제거
unique_links = list(set(links))

# 출력
for link in unique_links:
  print(link)
