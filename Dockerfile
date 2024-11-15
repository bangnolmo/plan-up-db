# Ubuntu 기반 이미지
FROM ubuntu:20.04

# 환경 설정
ENV DEBIAN_FRONTEND=noninteractive

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    software-properties-common \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    xvfb

# Google Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Chrome 버전 확인 (디버깅용)
RUN google-chrome --version || echo "Chrome installation failed"

# ChromeDriver 설치 (Chrome 버전에 맞춤)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    rm chromedriver-linux64.zip && \
    mv chromedriver-linux64 /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

# Python Selenium 설치
RUN pip3 install selenium

# 기본 작업 디렉토리 설정
WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# 스크립트 복사
COPY . .

# 실행 명령어
CMD ["python3", "./src/crawl_major_classes.py"]



