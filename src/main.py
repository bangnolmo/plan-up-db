import requests
import time

from datetime import datetime
from dotenv import load_dotenv
from src.parser.crawl_department_code import get_all_hakgwa_code
from src.parser.crawl_general_classes import get_all_jojik, get_all_general_classes
from src.parser.crawl_major_classes import get_all_major_classes
from src.utils.utils import get_chrome_driver_with_login, close_driver
from src.utils.utils import BACK_URL, CRAWL_AUTH


load_dotenv()

s_time = time.time()

# 드라이버 초기화
driver = get_chrome_driver_with_login()

now = datetime.now()
year = now.year
hakgi = 0

if now.month < 7:
    hakgi = 10
else:
    hakgi = 20

# 교양 조직 데이터 가져오기 (여기는 request만 테스트 수행)
all_jojik = get_all_jojik(driver, year, hakgi)
si = len(all_jojik)

print("교양 조직 구하기 완료")

# 교양 구분자 추가하기
for i in range(si):
    all_jojik[i].append(1)

# 학과 데이터 가져오기 (여기 부터해야 selenium 테스트 가능.
get_all_hakgwa_code(all_jojik, year, hakgi)

print("학과 조직 구하기 완료")

# 교양 과목 가져오기
all_class = get_all_general_classes(driver, year, hakgi)

print("모든 교양 과목 구하기 완료")

# 전공 과목 가져오기
for i in range(si, len(all_jojik)):
    # 전공 구분자 추가하기
    all_jojik[i].append(2)
    get_all_major_classes(driver, all_class, year, hakgi, all_jojik[i][1])

print("모든 전공 과목 구하기 완료")

# 드라이버 종료
close_driver(driver)

# 총 실행 시간 확인 하기
e_time = time.time()
print(f'총 실행 시간 : {e_time - s_time:.3f}')

# 백엔드 서버로 데이터 전송하기
return_json = {
    'auth': CRAWL_AUTH,
    'year': year,
    'hakgi': hakgi,
    'jojik': all_jojik,
    'classes': all_class
}

requests.put(BACK_URL, json=return_json)
