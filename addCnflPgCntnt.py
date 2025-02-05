import requests
from confluence_config import base_confluence_url, space_key, headers
import random
from getCnflPgId import get_page_id_by_title


def create_new_page(title, content):
  """새 페이지 생성 - 구조 상 특정 상위 페이지 하위에 생성"""

  # 등록되어야 할 메인 페이지 정보 조회
  # getCnflPgId 의 get_page_id_by_title() 로 페이지id 조회
  main_page_title = "scrapping test"
  ancestors_id = get_page_id_by_title(main_page_title)
  print(f"-> ancestors_id: {ancestors_id}")

  # 조회된 메인 페이지 하위에 신규 페이지 생성
  data = {
    "title": title,
    "type": "page",
    "ancestors":[{"id": ancestors_id}],
    "space": {"key": space_key},
    "body": {
      "storage": {
        "value": content,
        "representation": "storage"
      }
    }
  }
  print(f"-> data: {data}")  

  response = requests.post(base_confluence_url, headers=headers, json=data)
  if response.status_code == 200:
    print("new page created successfully")
  else:
    raise Exception(f"failed to create new page: {response.status_code}")






##########################################
# 직접 실행 가능하도록 추가 
# - 다른 파일에서 import 하여 호출 시 아래 내용은 실행되지 않음
# 실행 방법: python3 addCnflPgCntnt.py
##########################################
if __name__ == "__main__":
  # 랜덤한 5자리 정수 생성
  random_number = random.randint(10000, 99999)

  title = "new test " + str(random_number)
  print(f"-> title: {title}")
  content = "this is a test ... "

  try:
    print(f"creating for '{title}' on confluence ...")
    create_new_page(title, content)
  except Exception as e:
    print(f"error: {e}")