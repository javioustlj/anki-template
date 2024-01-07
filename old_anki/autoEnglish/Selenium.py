import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def add_notes_vocabulary(records):
    driver = webdriver.Chrome()
    driver.get("https://www.vocabulary.com/login/")

    element = driver.find_element_by_name("username")
    element.send_keys("tianlijian2012@163.com")
    element = driver.find_element_by_name("password")
    element.send_keys("tianlijian001")
    element = driver.find_element_by_tag_name("button")
    element.send_keys(Keys.RETURN)
    driver.get("https://www.vocabulary.com/lists/6695167/edit")
    js = '''
        var wordInputs;
        wordInputs = document.querySelectorAll(".wordInput");
        return wordInputs.length;
    '''
    res = driver.execute_script(js)
    for record in records:
        expression = record['expression']
        sentence = record['sentence']
        xpath = '//*[@id="wordlist"]/li[{0}]/div[1]/input'.format(res+1)
        print(res+1)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.send_keys(expression)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wordlist"]/li[{0}]/div[4]/ol/li[1]/div/span[2]'.format(res+1)))
        )
        element.send_keys(Keys.ENTER)
        xpath = '//*[@id="wordlist"]/li[{0}]/div[3]/div[1]/div/textarea'.format(res+1)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        js = 'arguments[0].value = arguments[1]'
        driver.execute_script(js, element, sentence)
        time.sleep(1)
        res += 1

def main():
    with open('test.json', 'r') as f:
        notes = json.loads(f.read())
    add_notes_vocabulary(notes)

if __name__ == '__main__':
    main()