from getCnflPgId import get_page_id_by_title
from putCnflPgCntnt import update_page_content
from addCnflPgCntnt import create_new_page

def manage_confluence_page(title, content):
  """confluence 페이지 관리 (기존 업데이트 또는 새로 생성)"""
  try:
    # 제목으로 페이지id 조회
    page_id = get_page_id_by_title(title)

    if page_id:
      # 기존 페이지 업데이트
      print(f"updating existing page: {title}")
      update_page_content(page_id, content)
    else:
      # 새로운 페이지 생성
      print(f"creating new page: {title}")
      create_new_page(title, content)
  except Exception as e:
    print(f"error managing confluence page: {e}")





##########################################
# 직접 실행 가능하도록 추가 
# - 다른 파일에서 import 하여 호출 시 아래 내용은 실행되지 않음
# 실행 방법: python3 setCnflMgmt.py
##########################################
if __name__ == "__main__":
  title = "new page1"
  content = "this is a test ..... "

  try:
    print(f"checking for {title} on confluence ...")
    manage_confluence_page(title, content)
  except Exception as e:
    print(f"error: {e}")