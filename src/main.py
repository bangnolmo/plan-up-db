import requests

from dotenv import load_dotenv
from src.parser.crawl_department_code import get_all_hakgwa_code
from src.parser.crawl_general_classes import get_all_jojik, get_all_general_classes
from src.parser.crawl_major_classes import get_all_major_classes
from src.utils.utils import get_chrome_driver_with_login, close_driver
from src.utils.utils import BACK_URL
import time


load_dotenv()

s_time = time.time()

# 드라이버 초기화
driver = get_chrome_driver_with_login()

# 교양 조직 데이터 가져오기 (여기는 request만 테스트 수행)
all_jojik = get_all_jojik(driver, 2024, 20)
si = len(all_jojik)

# 교양 구분자 추가하기
for i in range(si):
    all_jojik[i].append(1)

# 학과 데이터 가져오기 (여기 부터해야 selenium 테스트 가능.
get_all_hakgwa_code(all_jojik, 2024, 20)

# TODO -------- 배포시 주석 풀기 -----
# # 교양 과목 가져오기
# all_class = get_all_general_classes(driver, 2024, 20)
#
# # 전공 과목 가져오기
# for i in range(si, len(all_jojik)):
#     # 전공 구분자 추가하기
#     all_jojik[i].append(2)
#     get_all_major_classes(driver, all_class, 2024, 20, all_jojik[i][1])
# TODO --------여기 까지 ---------------------


# 드라이버 종료
close_driver(driver)

# 총 실행 시간 확인 하기
e_time = time.time()
print(f'실행 시간 : {e_time - s_time:.3f}')


# test 용 출력 - 현재 모든 조직을 받아서 출력 -> 실제 CI/CD 할 때에는
print(f'jojik : {len(all_jojik)}')
# print(f'class : {len(all_class)}')


# TODO -------- 배포시 주석 풀기 -----
# # 백엔드 서버로 데이터 전송하기
# return_json = {
#     'year': 2024,
#     'hakgi': 20,
#     'jojik': all_jojik,
#     'classes': all_class
# }
#
# requests.post(BACK_URL, json=return_json)
# TODO --------여기 까지 ---------------------
