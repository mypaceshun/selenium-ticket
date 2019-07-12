import os
import sys
import time
import chromedriver_binary  # noqa: F401
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'https://ticket.line.me/'

RETRY_COUNT = 3

# Artistsページからの検索が優先
ARTIST_NUMBER = os.environ.get('ARTIST_NUMBER', None)
EVENT_NUMBER = os.environ.get('EVENT_NUMBER', 2285)
EVENT_SEARCH_FILTER = {'DAY': os.environ.get('EVENT_DAY', '05.29'),
                       'NUM': int(os.environ.get('EVENT_NUM', 1))}
TICKET_TYPE_FILETER = {'TYPE': os.environ.get('TICKET_TYPE', 'シーティング')}
TICKET_NUM = {'ADULT': int(os.environ.get('TICKET_NUM_ADULT', 2)),
              'STUDENT': int(os.environ.get('TICKET_NUM_STUDENT', 0))}

USERID = os.environ.get('USERID', 'userid')
PASSWORD = os.environ.get('PASSWORD', 'password')

QUICK = os.environ.get('QUICK', False)


def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    event_list = fetch_event_list(driver)
    event = search_event(event_list)
    get_ticket(driver, event)
    print('ここまでやってあげたから後は頑張って[Enter]:', end="")
    input()


def fetch_event_list(driver):
    url = None
    if ARTIST_NUMBER is None:
        url = '{}events/{}'.format(BASE_URL, EVENT_NUMBER)
    else:
        url = '{}artists/{}'.format(BASE_URL, ARTIST_NUMBER)
    driver.get(url)
    a_els = []
    for i in range(RETRY_COUNT):
        a_els = driver.find_elements(By.CLASS_NAME, 'mdPerformanceListItem')
        if len(a_els) > 0:
            break
        time.sleep(1)
    event_list = []
    for a_el in a_els:
        url = a_el.get_attribute('href')
        text = a_el.text
        event_list.append({'url': url, 'text': text})
    return event_list


def search_event(event_list):
    daystr = EVENT_SEARCH_FILTER['DAY']
    search_event_list = [e for e in event_list if e['text'].startswith(daystr)]
    if len(search_event_list) < EVENT_SEARCH_FILTER['NUM']:
        msg = 'EVENT_SEARCH_FILTER[\'NUM\'] out of range [{}]'
        sys.stderr.write(msg.format(len(search_event_list)))
        exit(1)
    return search_event_list[EVENT_SEARCH_FILTER['NUM'] - 1]


def get_ticket(driver, event):
    driver.get(event['url'])
    ticket_type = TICKET_TYPE_FILETER['TYPE']
    ticket_els = []
    for i in range(RETRY_COUNT):
        class_name = 'mdMultiTicketTypeSeatItemInner'
        ticket_els = driver.find_elements(By.CLASS_NAME, class_name)
        if len(ticket_els) > 0:
            break
        time.sleep(1)

    is_enable_el = driver.find_elements(By.CLASS_NAME, 'ExDisabled')
    if len(is_enable_el) > 0:
        msg = '予定枚数終了しました'
        sys.stderr.write(msg)
        exit(1)

    search_ticket_list = [e for e in ticket_els if ticket_type in e.text]
    if len(search_ticket_list) == 0:
        msg = 'ticket_type[{}] is not found'.format(ticket_type)
        sys.stderr.write(msg)
        exit(1)
    search_ticket = search_ticket_list[0]
    search_ticket.click()

    # LINEログイン
    userid_el = None
    for i in range(RETRY_COUNT):
        userid_el = driver.find_element(By.NAME, 'tid')
        if userid_el is not None:
            break
        time.sleep(1)
    passwd_el = driver.find_element(By.NAME, 'tpasswd')
    submit_el = driver.find_element(By.CLASS_NAME, 'mdFormGroup01Btn')

    userid_el.send_keys(USERID)
    passwd_el.send_keys(PASSWORD)
    submit_el.click()

    # 枚数選択画面
    ticket_num_els = []
    for i in range(RETRY_COUNT):
        ticket_num_els = driver.find_elements(By.CLASS_NAME, 'mdDropdownInner')
        if len(ticket_num_els) > 0:
            break
        time.sleep(1)
    if TICKET_NUM['ADULT'] > 0:
        ticket_num_els[0].click()
        options_els = driver.find_elements(By.CLASS_NAME, 'mdDropdownItem')
        if len(options_els) - 1 < TICKET_NUM['ADULT']:
            msg = 'ticket_num[ADULT] out of range [{}]'
            sys.stderr.write(msg.format(len(options_els) - 1))
            exit(1)
        options_els[TICKET_NUM['ADULT']].click()

    if TICKET_NUM['STUDENT'] > 0:
        ticket_num_els[1].click()
        options_els = driver.find_elements(By.CLASS_NAME, 'mdDropdownItem')
        if len(options_els) - 1 < TICKET_NUM['STUDENT']:
            msg = 'ticket_num[ADULT] out of range [{}]'
            sys.stderr.write(msg.format(len(options_els) - 1))
            exit(1)
        options_els[TICKET_NUM['STUDENT']].click()

    submit_el = driver.find_element(By.CLASS_NAME, 'MdButton')
    submit_el.click()

    if QUICK:
        # 0秒で確認しな
        pass
    else:
        # 3秒で確認しな
        time.sleep(3)
    submit_els = driver.find_elements(By.CLASS_NAME, 'MdButton')
    submit_els[1].click()

    # 支払い方法選択
    radio_els = []
    for i in range(RETRY_COUNT):
        radio_els = driver.find_elements(By.CLASS_NAME, 'mdRadioButtonRadio')
        if len(radio_els) > 0:
            break
        time.sleep(1)
    radio_els[1].click()  # クレカ
    submit_el = driver.find_element(By.CLASS_NAME, 'MdButton')
    submit_el.click()


if __name__ == '__main__':
    main()
