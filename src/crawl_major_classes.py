import os
import re
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from login import login

# get env
load_dotenv()
user_id = os.getenv("ST_ID")
user_pw = os.getenv("ST_PW")

base_url = "https://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp"


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


def go_to_schedule_page(driver, curPage, gyear, ghakgi, hakgwa_cd, gwamok_name=""):
    """
    동적으로 URL을 생성하고 해당 페이지로 이동.

    :param driver: Selenium WebDriver 인스턴스
    :param curPage: 현재 페이지 번호 (페이지네이션)
    :param gyear: 조회할 년도
    :param ghakgi: 학기 정보 (10: 1학기, 20: 2학기)
    :param hakgwa_cd: 학과 코드
    :param gwamok_name: 과목명 (옵션, 기본은 빈 문자열)
    """
    url = f"{base_url}?curPage={curPage}&gyear={gyear}&ghakgi={ghakgi}&hakgwa_cd={hakgwa_cd}&gwamok_name={gwamok_name}"
    driver.get(url)
    get_schedule_list(driver, hakgwa_cd)

    total_page = get_total_pages(driver)
    if total_page is not None:
        sub_schedule_page(driver, total_page, gyear, ghakgi, hakgwa_cd, gwamok_name="")


def sub_schedule_page(driver, total_page, gyear, ghakgi, hakgwa_cd, gwamok_name=""):
    """
    페이지 하나씩 증가하여 개강과목을 가져오기

    :param driver: Selenium WebDriver 인스턴스
    :param total_page: 총 페이지 번호
    :param gyear: 조회할 년도
    :param ghakgi: 조회할 학기
    :param hakgwa_cd: 학과 코드
    :param gwamok_name: 과목명
    :return:
    """
    for curPage in range(2, total_page + 1):
        url = f"{base_url}?curPage={curPage}&gyear={gyear}&ghakgi={ghakgi}&hakgwa_cd={hakgwa_cd}&gwamok_name={gwamok_name}"
        driver.get(url)
        get_schedule_list(driver, hakgwa_cd)


def get_all_major_classes(data, year, hakgi):
    # init driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # GPU 비활성화 (headless에서 필요)
    options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
    options.add_argument("--start-maximized")  # 최대화된 창으로 시작
    options.add_argument("--disable-software-rasterizer")  # 소프트웨어 렌더링 비활성화

    # WebDriver 초기화
    # service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=options)

    driver.get("https://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp")
    time.sleep(1)

    # login
    login(driver, user_id, user_pw)

    # start crawling
    go_to_schedule_page(driver, 1, year, hakgi, data[0])

    driver.quit()
    pass


if __name__ == "__main__":
    get_all_major_classes(['85511'], 2024, 20)