import os
import time

from dotenv import load_dotenv
from selenium import webdriver

from src.utils.utils import login

# get env
load_dotenv()
user_id = os.getenv("ST_ID")
user_pw = os.getenv("ST_PW")

base_url = "https://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp"



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