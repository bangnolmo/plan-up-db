from src.utils.utils import get_chrome_driver_with_login, close_driver
from src.utils.utils import get_schedule_list
from src.utils.utils import get_total_pages


major_base_url = "https://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu222s.jsp"


def sub_schedule_page(driver, res, total_page, gyear, ghakgi, hakgwa_cd, gwamok_name=""):
    """
    페이지 하나씩 증가하여 개강과목을 가져오기

    :param driver: Selenium WebDriver 인스턴스
    :param res: 파싱 데이터를 저장할 list
    :param total_page: 총 페이지 번호
    :param gyear: 조회할 년도
    :param ghakgi: 조회할 학기
    :param hakgwa_cd: 학과 코드
    :param gwamok_name: 과목명
    :return:
    """

    for curPage in range(1, total_page + 1):
        url = f"{major_base_url}?curPage={curPage}&gyear={gyear}&ghakgi={ghakgi}&hakgwa_cd={hakgwa_cd}&gwamok_name={gwamok_name}"
        driver.get(url)
        get_schedule_list(driver, res, hakgwa_cd)


def go_to_schedule_page(driver, res, gyear, ghakgi, hakgwa_cd, gwamok_name=""):
    """
    동적으로 URL을 생성하고 해당 페이지로 이동.

    :param driver: Selenium WebDriver 인스턴스
    :param res: 파싱 데이터를 저장할 list
    :param gyear: 조회할 년도
    :param ghakgi: 학기 정보 (10: 1학기, 20: 2학기)
    :param hakgwa_cd: 학과 코드
    :param gwamok_name: 과목명 (옵션, 기본은 빈 문자열)
    """

    # 총 페이지 획득
    url = f"{major_base_url}?curPage=1&gyear={gyear}&ghakgi={ghakgi}&hakgwa_cd={hakgwa_cd}&gwamok_name={gwamok_name}"
    driver.get(url)
    total_page = get_total_pages(driver)

    if total_page is not None:
        sub_schedule_page(driver, res, total_page, gyear, ghakgi, hakgwa_cd, gwamok_name="")


def get_all_major_classes(driver, hakgwa_cd_list, res, year, hakgi):
    # start crawling
    for d in hakgwa_cd_list:
        go_to_schedule_page(driver, res, year, hakgi, d)


if __name__ == "__main__":
    parse_data = []

    driver = get_chrome_driver_with_login()
    get_all_major_classes(driver, ['85511'], parse_data, 2024, 20)
    close_driver(driver)

    for r in parse_data:
        print(r)