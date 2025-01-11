import requests
import json
from datetime import datetime, timedelta

# 구글 api 키, 검색엔진 id
GOOGLE_API_KEY='AIzaSyBa80M29IKMNBiZNdn0JSf1r-5at4rROIc'
GOOGLE_CSE_ID='b0b6a7dd22d6942ed'
search_url = 'https://www.googleapis.com/customsearch/v1'

# 검색 키워드
search_query = '서평단 모집'
date_limit = 30   # 30일 이내

# 오늘 날짜와 30일 전 날짜 계산
today = datetime.today()
start_date = today - timedelta(days=date_limit)
start_date_str = start_date.strftime('%Y-%m-%d')

# 구글 검색 api 호출
def fetch_urls():
  urls = []
  page = 1
  while True:
    params = {
      'key': GOOGLE_API_KEY,
      'cx': GOOGLE_CSE_ID,
      'q': search_query,
      'dateRestrict': f'd{date_limit}',
      'start': (page - 1) * 10  + 1     # 페이지당 10개 결과
    }
    print(f"params: {params}")

    response = requests.get(search_url, params=params)
    print(f"response: {response}")
    data = response.json()
    print(f"data: {data}")
    if 'items' in data:
      for item in data['items']:
        urls.append(item['link'])
      if 'nextPage' in data.get('queries', {}):
        page += 1
      else:
        break
    else:
      break
  return urls


if __name__ == '__main__':
  urls = fetch_urls()
