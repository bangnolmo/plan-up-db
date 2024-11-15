import re
from dataclasses import dataclass
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def make_url(cd, action):
    """
    학과명 와 학과 코드를 파싱하기 위한 URL 획득
    :param cd: 학과 코드
    :param action: expand or fold (하위학과 요청 파라미터
    :return: 최종 요청 URL
    """
    year = datetime.today().year
    month = datetime.today().month

    # 1학기의 경우 hakgi=10, 2학기의 경우 hakgi=20
    hakgi = 10
    if month >= 8:
        hakgi = 20

    # gubun : 학사(1), 석사로 나뉘어져 있는 거 같음.
    gubun = 1
    return (f'https://kutis.kyonggi.ac.kr/webkutis/view/hs/wsco2/wscoHagwaTreeSU.jsp?'
            f'year={year}&hakgi={hakgi}&gubun={gubun}&hakgwa_cd={cd}&action_gubun={action}')


def check_format(size, check_size):
    """
    사이트의 구조가 바뀌었는지 확인하는 함수
    :param size: 파싱을 통해 얻느 데이터의 크기
    :param check_size: 실제 얻어야 하는 데이터의 크기
    :return: None
    :exception: 학과 트리 구조가 바뀌었다는 에러 발생
    """
    if size != check_size:
        raise ValueError("학과 트리 구조가 바뀌었습니다.")


def get_all_hakgwa_code(arr, prefix='', depth=0, before=0, url=make_url('A1000', 'expand')):

    res = requests.post(url)

    if res.status_code != 200:
        raise ValueError("쿠티스 서버 연결 실패")

    soup = BeautifulSoup(res.text, 'html.parser')

    # get all_elements
    # 하나의 tr에 하나의 학과가 들어가 있음.
    all_elements = soup.find_all('tr')

    for i in range(depth, len(all_elements) - before):
        # 하나의 tr 태그를 파싱
        a_tag = all_elements[i].find_all('a')
        check_format(len(a_tag), 2)

        data = re.sub(r"[')]", '', a_tag[0]['href']).split(',')
        check_format(len(data), 4)

        # 대학및 학과 이름과 코드 획득
        name = data[-1].split("-")[1]
        code = data[1]

        # [-1] row data : '1') or '2') -> '1' or '2'로 변환
        stat = a_tag[1]['href'].split(',')[-1].replace(')', '').replace("'", '')

        # 1 의미 : 더 확장 가능 (대학을 의미), 2 의미 : 더 확장 불가 (학과를 의미)
        if stat == '1':
            new_pre = prefix + '-' + name
            get_all_hakgwa_code(arr, new_pre, i + 1, len(all_elements) - i - 1, make_url(code, 'fold'))
        elif stat == '2':
            # 학과 데이터 추가
            arr.append((code, prefix[1:] + '-' + name))
        else:
            # 1와 2가 아닌 경우 : 트리 format 이 바뀌었음을 의미
            check_format(0, 1)





if __name__ == "__main__":
    res = []
    get_all_hakgwa_code(res)
    for d in res:
        print(d)