from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from src.utils.utils import get_schedule_list, get_chrome_driver_with_login, close_driver


general_base_url = "https://kutis.kyonggi.ac.kr/webkutis/view/hs/wssu2/wssu221s.jsp"


def set_year_and_hakgi(driver, gyear, ghakgi):
    """
    현재 페이지에서 년도와 학기 선택

    :param driver: Selenium WebDriver 인스턴스
    :param gyear: 설정할 년도
    :param ghakgi: 설정할 학기
    """

    # 년도 설정
    year_input = driver.find_element(By.XPATH, '//*[@name="gyear"]')
    year_input.clear()
    year_input.send_keys(gyear)

    # 학기 설정
    ghakgi_group = driver.find_element(By.NAME, 'ghakgi')
    ghakgis = Select(ghakgi_group)
    for hakgi in ghakgis.options:
        if hakgi.get_attribute("value") == str(ghakgi):
            hakgi.click()
            break


def get_all_jojik(driver, gyear, ghakgi):
    """
    모든 교양 과목 시간대 구분 파싱하기

    :param driver: Selenium WebDriver 인스턴스
    :param gyear: 조회활 년도
    :param ghakgi: 조화힐 학기
    :return: [[year, hakgi, jojik_name] ...]
    """

    result = []

    driver.get(general_base_url)
    while driver.execute_script("return document.readyState") != "complete":
        pass

    set_year_and_hakgi(driver, gyear, ghakgi)

    jojiks = Select(driver.find_element(By.NAME, 'jojik_group')).options

    for jojik in jojiks:
        if jojik.text == "전체":
            continue
        result.append([jojik.text, jojik.get_attribute('value')])

    return result


def get_all_general_classes(driver, gyear, ghakgi):
    """
    모든 교양 과목 조회하기

    :param driver: Selenium WebDriver 인스턴스
    :param gyear: 조회할 년도
    :param ghakgi: 조회할 학기
    :return: [[명세서 참조 부탁합니다. 명시하기에 너무 많음.]...]
    """

    driver.get(general_base_url)
    while driver.execute_script("return document.readyState") != "complete":
        pass

    set_year_and_hakgi(driver, gyear, ghakgi)

    result = []

    i = 0
    while True:
        # 조직 설정
        jojiks = Select(driver.find_element(By.NAME, 'jojik_group')).options

        i += 1
        if i == len(jojiks):
            break

        jojik = jojiks[i]
        jojik_code = jojik.get_attribute('value')

        jojik.click()

        # 검색
        driver.find_element(By.XPATH, '//*[text()="조회"]').click()

        # print(get_total_pages(driver))
        get_schedule_list(driver, result, jojik_code)

    # 전공 과목의 포멧과 맞추기 위함.
    renew_data = []
    for r in result:
        renew_data.append(r[1:])
        renew_data[-1][0] = r[0]

    return renew_data


if __name__ == "__main__":
    driver = get_chrome_driver_with_login()

    # result = get_all_jojik(driver, 2024, 20)
    #
    # print(result[0])

    res = get_all_general_classes(driver, 2024, 10)
    print(res[0])
    close_driver(driver)
    #
    # for r in res:
    #     print(r)