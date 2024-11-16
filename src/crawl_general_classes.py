import os
import re
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from login import login

# get env
load_dotenv()
user_id = os.getenv("ST_ID")
user_pw = os.getenv("ST_PW")

base_url = "https://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu221s.jsp"


def get_total_pages(driver):
    """
    현재 URL에서 개강된 과목 총 페이지수를 획득.

    :param driver: Selenium WebDriver 인스턴스
    :return: 총 페이지 수 or None(총 페이지 수 못 찾은 경우)
    """

    try:
        element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/p")
    except:
        return None

        # 예시: "총 :3 page"
    text = element.text

    # 정규식을 사용해 숫자 부분 추출
    match = re.search(r"총 :(\d+) page", text)

    if match:
        total_pages = int(match.group(1))
        return total_pages
    else:
        return None


def go_to_schedule_page(res, driver, gyear, ghakgi):
    url = base_url
    driver.get(url)

    # 년도 설정
    year_input = driver.find_element(By.XPATH, '//*[@name="gyear"]')
    year_input.clear()
    year_input.send_keys(gyear)

    # 학기 설정
    ghakgi_group = driver.find_element(By.NAME, 'ghakgi')
    ghakgis = Select(ghakgi_group)
    for hakgi in ghakgis.options:
        print(hakgi.get_attribute("value"))
        if hakgi.get_attribute("value") == str(ghakgi):
            hakgi.click()
            break

    i = 0
    while True:
        # 조직 설정
        jojiks = Select(driver.find_element(By.NAME, 'jojik_group')).options

        i += 1
        if i == len(jojiks):
            break

        jojik = jojiks[i]

        jojik.click()

        # 검색
        driver.find_element(By.XPATH, '//*[text()="조회"]').click()

        # print(get_total_pages(driver))
        get_schedule_list(driver, '')
        

def get_schedule_list(driver, hakgwa_cd):
    """
    학과 코드에 따른 시간표 데이터를 추출하여 DB에 삽입하는 함수.

    :param driver: Selenium WebDriver 인스턴스
    :param hakgwa_cd: 학과 코드
    """

    # 모든 tbody 요소 가져오기
    tbodies = driver.find_elements(By.XPATH, '//table[@class="list02"]/tbody')

    # 각 tbody에서 데이터를 추출
    for tbody in tbodies:
        rows = tbody.find_elements(By.TAG_NAME, "tr")  # tbody 내 모든 tr 요소 가져오기
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            # 데이터 생성
            row_data = [hakgwa_cd]

            for col in cols:
                row_data.append(col.text.replace("\n보기", '').strip())

            # TODO DB에 출력 또는 arr에 저장하는 로직 필요
            print(row_data)


def get_all_general_classes(res, year, hakgi):
    # init driver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")  # GPU 비활성화 (headless에서 필요)
    # options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
    # options.add_argument("--start-maximized")  # 최대화된 창으로 시작
    # options.add_argument("--disable-software-rasterizer")  # 소프트웨어 렌더링 비활성화

    # WebDriver 초기화
    # service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=options)

    driver.get("https://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp")
    time.sleep(1)

    # login
    login(driver, user_id, user_pw)

    # start crawling
    go_to_schedule_page(res, driver, year, hakgi)

    driver.quit()
    pass


if __name__ == "__main__":
    res = []
    get_all_general_classes(res,2024, 10)

    for r in res:
        print(r)