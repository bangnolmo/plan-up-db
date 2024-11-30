from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def login(driver, user_id, user_pw):
    """
    selenium을 kutis에 로그인하기

    :param driver: chrome driver
    :param user_id: 학생 ID
    :param user_pw: 학생 PW
    """

    driver.get("https://kutis.kyonggi.ac.kr/webkutis/view/indexWeb.jsp")
    while driver.execute_script("return document.readyState") != "complete":
        pass

    input_id = driver.find_element(By.XPATH, '//*[@id="id"]')
    input_pw = driver.find_element(By.XPATH, '//*[@id="pw"]')

    input_id.send_keys(user_id)
    input_pw.send_keys(user_pw)
    input_pw.send_keys(Keys.RETURN)



if __name__ == "__main__":
    pass