from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests
import json

# Google Chat Webhook URL 설정 (생성한 URL로 변경)
webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA74byHYI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=N3ItbavstbCp7Sj0blOp92kBKxGz2_OAGih10GyitQs'

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://c-tas.krcert.or.kr")
    driver.find_element(By.NAME, 'userId').send_keys('hungu1023')
    driver.find_element(By.NAME, 'userPassword').send_keys('Sniper123!@#')

    login_button = driver.find_element(By.CLASS_NAME, 'btn_log')
    login_button.click()

    # 로그인 후 페이지 로딩을 기다림
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("https://c-tas.krcert.or.kr"))

    # 로그인 후 이동할 페이지 URL
    desired_url = "https://c-tas.krcert.or.kr/board/notice/securityList"
    driver.get(desired_url)

    # 오늘 날짜 형식 설정
    today = datetime.today().strftime('%Y.%m.%d')

    # 키워드 목록 설정
    keywords = ["Cisco", "github", "gitlab", "fortinet", "Apache Flnik"]
    messages = []

    # 게시글 아이템 가져오기
    items = driver.find_elements(By.XPATH, "//tbody[@id='noticeList']/tr")
    for item in items:
        title_element = item.find_element(By.CLASS_NAME, 'title')
        title = title_element.text.strip()
        date = item.find_element(By.CLASS_NAME, 'date').text.strip()
        link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # 오늘 게시된 글 중 키워드 포함된 글 찾기
        if today in date and any(keyword.lower() in title.lower() for keyword in keywords):
            messages.append(f"제목: {title}, 링크: {link}")

    initial_message = "[보안 업데이트 권고]"
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {
        "text": initial_message
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Initial message sent to Google Chat")
    else:
        print(f"Error sending initial message to Google Chat: {response.status_code}")

    # 수집한 데이터를 Google Chat으로 전송
    if messages:
        message_text = "\n".join(messages)
    else:
        message_text = "매칭된 게시글이 없습니다."

    data = {
        "text": message_text
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Message sent to Google Chat")
    else:
        print(f"Error sending message to Google Chat: {response.status_code}")

    initial_message = "[보안 뉴스]"
    data = {
        "text": initial_message
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Initial message sent to Google Chat")
    else:
        print(f"Error sending initial message to Google Chat: {response.status_code}")

    desired_url = "https://c-tas.krcert.or.kr/security/news/list"
    driver.get(desired_url)

    # 카드형 게시판 리스트 요소 찾기
    card_list = driver.find_element(By.ID, 'cardList')

    # 카드 리스트 내의 각 항목(li) 요소 추출
    items = card_list.find_elements(By.TAG_NAME, 'li')

    # 오늘 날짜의 제목 추출 및 출력
    for item in items:
        date = item.find_element(By.CLASS_NAME, 'date').text
        title = item.find_element(By.CLASS_NAME, 'sbj').text
        link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

        if date == today:
            print(title)
            messages.append(f"제목: {title}, 링크: {link}")

    if messages:
        message_text = "\n".join(messages)
    else:
        message_text = "매칭된 게시글이 없습니다."

    data = {
        "text": message_text
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Message sent to Google Chat")
    else:
        print(f"Error sending message to Google Chat: {response.status_code}")

finally:
    driver.quit()
