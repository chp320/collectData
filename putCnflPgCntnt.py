import requests
from confluence_config import base_confluence_url, headers

def update_page_content(page_id, content):
  """기존 페이지에 콘텐츠 업데이트"""
  page_url = f"{base_confluence_url}/{page_id}"

  # 페이지id 로 페이지 정보 조회
  response = requests.get(page_url, headers=headers)
  if response.status_code != 200:
    raise Exception(f"failed to fetch page details: {response.status_code}")

  page_data = response.json()
  print(f"-> page_data: {page_data}")
  version = page_data['version']['number'] + 1
  print(f"-> version: {version}")

  # 업데이트 데이터 구성
  data = {
    "version": {"number": version},
    "title": page_data['title'],
    "type": "page",
    "body": {
      "storage": {
        "value": content,
        "representation": "storage"
      }
    }
  }
  print(f"-> data: {data}")

  response = requests.put(page_url, headers=headers, json=data)
  if response.status_code == 200:
    print("page updated successfully.")
  else:
    raise Exception(f"failed to update page: {response.status_code}")






##########################################
# 직접 실행 가능하도록 추가 
# - 다른 파일에서 import 하여 호출 시 아래 내용은 실행되지 않음
# 실행 방법: python3 putCnflPgCntnt.py
##########################################
if __name__ == "__main__":
  page_id = "66187"
  content = "this is a test ... "

  try:
    print(f"putting for {page_id} on confluence ...")
    update_page_content(page_id, content)
  except Exception as e:
    print(f"error: {e}")