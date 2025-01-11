##########################################
# 구글 검색 결과 url 에서 링크 페이지 정보를 추출 후, 컨플루언스 페이지를 생성 혹은 수정 하는 기능
# - 메인 기능을 하고, 각 기능별 구현된 파일을 import 후 함수를 호출한다.
# 실행 방법: python3 startMain.py
##########################################

from datetime import datetime
from getGoogleRsltTest import extract_google_links
from setCnflMgmt import manage_confluence_page
import random

# 검색 키워드, 제한 날짜 설정
search_query = "서평단+모집"
today = datetime.now().strftime('%Y%m%d')
# 랜덤한 5자리 정수 생성
random_number = random.randint(10000, 99999)
page_title = f"{today} - {search_query}" + str(random_number)


if __name__ == "__main__":
  try:
    # 구글 검색 결과 링크 추출
    print("extracting google search results ...")
    links = extract_google_links(search_query)

    if not links:
      print("no links found.")
    else:
      # confluence 페이지 생성 또는 업데이트
      page_content = "<br>".join(links)     # html 형식으로 변경
      print("updaing confluence page ...")
      manage_confluence_page(page_title, page_content)
      print("task completed successfully")
  except Exception as e:
    print(f"error: {e}")