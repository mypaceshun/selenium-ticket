import os
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = 'https://ticket.line.me/'


def main():
    print(os.environ['USERNAME'])
    options = Options()
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(BASE_URL)
    driver.quit()


if __name__ == '__main__':
    main()
