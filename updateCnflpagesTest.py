#########################################################
# * 구글 검색 결과 페이지 결과에서 링크 url 추출 후 컨플루언스 페이지에 자동 등록하기
# * 상세 요건
# 1. 구글 검색 결과 페이지를 url 로 생성한다. (조회 조건은 쿼리스트링으로 삽입하고, 언제든 변경 가능하도록 변수 처리한다.)
# 2. 수집된 자료는 confluence cloud 의 페이지에 저장한다.
# 3. 페이지 제목은 날짜 및 검색 키워드로 작성하고 이미 생성된 제목이 있으면 기존 페이지에 업데이트 한다.
#    - 페이지 제목 예시: 2025.01.11 - 서평단 모집
# 4. 페이지 생성 및 수정은 confluence 에서 제공하는 api 를 호출해서 페이지에 기록한다.
# 5. 검색 키워드와 날짜 제한은 변수 처리하여 언제든 변경 가능해야 한다.
# 6. 작업해야 하는 confluence 주소는 다음과 같다.
#    - myhope.atlassian.net
# 7. 스페이스는 chp320 이고, 해당 스페이스 하위에 페이지를 생성해야 한다.
#########################################################
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 검색 키워드
search_query = "서평단+모집"
# 날짜 포맷
today = datetime.now().strftime('%Y.%m.%d')
page_title = f"{today} - {search_query}"

# 구글 검색 결과 페이지 url
base_url = f"https://www.google.com/search?q=intitle:%22{search_query}%22&as_qdr=m"
print(f"base_url: {base_url}")

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
print(f"unique_links: {unique_links}")


# Confluence API 설정
base_confluence_url = "https://myhope.atlassian.net/wiki/rest/api/content"
space_key = "test"
encoded_api_token = "Y2hwMzIwQG5hdmVyLmNvbTpBVEFUVDN4RmZHRjA2VEIwdFpoblhEbWdwMlVRRjRkc0JzYkpvUFR4M0VrUEtnOWcyUHNwYllOa25aVUVsRm5sUUlKZUJBMmVUNk9tNVBLc2lubzFiNmFRUk5sMWdzOEhfUjBkWkRRMWs2SUVRUE8xVUV1ZWl3YTZPTzRpckJPaHR0LW1LM1VQRnBzOFcyWWhlRzB2b0kydlUtREpROFNOUE9xbUVGRG9yeDJmUmprSFN4V2RuWU09Mzc4NUE0QUY="

# confluence api header 설정
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Basic {encoded_api_token}'
}

# 수집된 자료를 confluence 페이지에 저장 및 업데이트
def create_or_update_confluence_page(title, content):

  print("create_or_update_confluence_page start...")

  # api url
  api_url = f"{base_confluence_url}?title={title}&spaceKey={space_key}"
  print(f"api_url: {api_url}")

  # 기존 페이지 존재 여부 검색
  search_url = f"{base_confluence_url}?title={title}&spaceKey={space_key}"
  response_search = requests.get(search_url, headers=headers)
  print(f"response_search.status_code: {response_search.status_code}")

  if response_search.status_code == 200:
    print("status code is 200")

    existing_pages = response_search.json()['results']

    # 페이지가 존재하는 경우 기존 페이지에 내용 추가
    if existing_pages:
      page_id = existing_pages[0]['id']
      # 기존 페이지 수정
      update_url = f"{base_confluence_url}/{page_id}"
      data = {
        "version": {
          "number": existing_pages[0]['version']['number'] + 1
        },
        "title": title,
        "space": {
          "key": space_key
        },
        "body": {
          "storage": {
            "value": content,
            "representation": "storage"
          }
        }
      }

      response_update = requests.put(update_url, headers=headers, json=data)
      if response_update.status_code == 200:
        print("page updated successfully")
      else:
        print(f"failed to update page: {response_update.status_code}")
    else:
      print("status code is not 200 ..")

      # 페이지 생성
      data = {
        "title": title,
        "space": {
          "key": space_key
        },
        "body": {
          "storage": {
            "value": content,
            "representation": "storage"
          }
        }
      }

      response_create = requests.post(base_confluence_url, headers=headers, json=data)
      if response_create.status_code == 201:
        print("page created successfully")
      else:
        print(f"failed to create page: {response_create.status_code}")

  print("create_or_update_confluence_page end...")


# 페이지 제목과 내용 설정
page_content = "\n\n".join(unique_links)
create_or_update_confluence_page(page_title, page_content)
