import requests
from bs4 import BeautifulSoup

def extract_google_links(search_query, time_range="m"):
  """구글 검색 결과에서 링크를 추출하는 함수."""
  base_url = f"https://www.google.com/search?q=intitle:%22{search_query}%22&as_qdr={time_range}"
  print(f"-> base_url: {base_url}")
  response = requests.get(base_url)
  if response.status_code != 200:
    raise Exception(f"Google search failed with status code - {response.status_code}")
  
  soup = BeautifulSoup(response.text, 'html.parser')
  links = []
  for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if href.startswith('/url?q='):
      real_link = href.split('/url?q=')[1].split('&')[0]
      links.append(real_link)

  # 중복 제거
  return list(set(links))

##########################################
# 직접 실행 가능하도록 추가 
# - 다른 파일에서 import 하여 호출 시 아래 내용은 실행되지 않음
##########################################
if __name__ == "__main__":
  # 테스트를 위한 검색 키워드
  search_query = "서평단+모집"
  # 검색 기간
  # 참고) as_qdr 가능한 값
  # - h: 지난 1시간 동안의 검색 결과
  # - d: 지난 하루 동안의 검색 결과
  # - w: 지난 1주 동안의 검색 결과
  # - w2: 지난 2주 동안의 검색 결과
  # - m: 지난 1개월 동안의 검색 결과
  # - m3: 지난 3개월 동안의 검색 결과
  # - y: 지난 1년 동안의 검색 결과
  time_range = "d3"

  try:
    print(f"searching for '{search_query}' on google ...")
    links = extract_google_links(search_query, time_range)
    if links:
      print("extracted links:")
      for link in links:
        print(link)
    else:
      print("no links found.")
  except Exception as e:
    print(f"error: {e}")