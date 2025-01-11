import requests
from confluence_config import base_confluence_url, space_key, headers

def get_page_id_by_title(title):
  """Confluence 에서 제목으로 페이지 id 조회"""
  search_url = f"{base_confluence_url}?title={title}&spaceKey={space_key}"
  response = requests.get(search_url, headers=headers)
  if response.status_code == 200:
    results = response.json().get('results', [])
    if results:
      return results[0]['id']
    else:
      return None
  else:
    raise Exception(f"failed to search page by title: {response.status_code}")




##########################################
# 직접 실행 가능하도록 추가 
# - 다른 파일에서 import 하여 호출 시 아래 내용은 실행되지 않음
# 실행 방법: python3 getCnflPgId.py
##########################################
if __name__ == "__main__":
  title = "new page1"

  try:
    print(f"searching for '{title}' on confluence ...")
    results = get_page_id_by_title(title)
    
    if results:
      print(f"result: {results}")
    else:
      print("no results found.")
  except Exception as e:
    print(f"error: {e}")