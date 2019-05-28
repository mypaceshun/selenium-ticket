
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    print('main')
    options = Options()
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://google.co.jp')
    driver.quit()


if __name__ == '__main__':
    main()
