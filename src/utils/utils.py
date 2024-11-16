import re

from selenium.webdriver.common.by import By


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


def get_schedule_list(driver, res, hakgwa_cd=''):
    """
    현재 페이지에서 시간표 데이터를 추출하여 반환

    :param driver: Selenium WebDriver 인스턴스
    :param hakgwa_cd: 학과 코드 / 교양의 경우 empty string
    :param res: 파싱하여 얻은 데이터를 저장하는 배열
    :return: 현재 시간표 데이터를 리스트로 반환 함.
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

            res.append(row_data)
    return res