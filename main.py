from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from retrying import retry


@retry(stop_max_attempt_number=30)
def launchSeleniumWebdriver(chrome_account):
    global driver
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-popup-blocking")
    # 用户个人资料路径
    option.add_argument(r'--user-data-dir=C:\Users\liangjun\AppData\Local\Google\Chrome\User Data')
    option.add_argument(f'--profile-directory={chrome_account}')
    driver = uc.Chrome(options=option)
    return driver


def checkAlert():
    while True:
        try:
            element = driver.find_element(By.XPATH, '//span[text()="Close"]')
        except NoSuchElementException:
            print("no alert")
            break
        else:
            driver.find_element(By.XPATH, '//span[text()="Close"]').click()
            break


def checkElement(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        print(f"no element {xpath}")
        return False
    else:
        return True


def conncetMetaMask():
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    inputs = driver.find_elements(By.XPATH, '//input')
    # MetaMask密码
    inputs[0].send_keys('qq535462548484xx?')
    driver.find_element(By.XPATH, '//button[text()="解鎖"]').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)


def connectPremint():
    flag = checkElement('//a[text()="Connect"]')
    if not flag:
        print("no connect button")
        return
    driver.find_element(By.XPATH, '//a[text()="Connect"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//a[@title="Twitter"]').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


def connectDiscord():
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://discord.com/channels/@me')
    time.sleep(3)
    flag = checkElement('//div[text()="登录"]')
    if not flag:
        print("no 登录 button")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return
    driver.find_element(By.XPATH, '//div[text()="登录"]').click()
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def register(num):
    for i in range (0, 3):
        try:
            # 打印打开第num个页面
            print(f'open page {num}')
            flag = checkElement('//button[@type="submit"]')
            if not flag:
                driver.close()
                return

            pre_element_list = driver.find_elements(By.XPATH, "//div[@class='card-body p-0']//a[@href]")
            premint_url_list = []
            # 通过a标签的href属性获取url，并存入列表
            for i in range(0, len(pre_element_list)):
                url = pre_element_list[i].get_attribute('href')
                premint_url_list.append(url)
            # 去重
            premint_url_list = list(set(premint_url_list))
            # 筛选链接的前缀
            twitter_url_list = [i for i in premint_url_list if i.startswith('https://twitter.com/')]
            dcord_url_list = [i for i in premint_url_list if i.startswith('https://discord.gg/')]
            # 进一步筛选retweet链接
            retweet_url_list = [i for i in twitter_url_list if 'user' in i]
            # 从twitter_url_list中去除retweet_url_list中的链接
            for i in retweet_url_list:
                twitter_url_list.remove(i)

            # 关注推特
            if len(twitter_url_list) > 0:
                for i in twitter_url_list:
                    driver.execute_script("window.open();")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(i)
                    time.sleep(2)
                    follow_flag = checkElement('//span[text()="Follow"]')
                    if follow_flag:
                        try:
                            driver.find_element(By.XPATH, '//span[text()="Follow"]').click()
                        except:
                            pass
                    time.sleep(1)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(1)
            # retweet&like
            if len(retweet_url_list) > 0:
                for i in retweet_url_list:
                    driver.execute_script("window.open();")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(i)
                    time.sleep(1)
                    retweet_flag = checkElement('//div[@aria-label="Retweet"]')
                    if retweet_flag:
                        driver.find_element(By.XPATH, '//div[@aria-label="Retweet"]').click()
                        time.sleep(1)
                        driver.find_element(By.XPATH, '//span[text()="Retweet"]').click()
                        time.sleep(1)
                    like_flag = checkElement('//div[@aria-label="Like"]')
                    if like_flag:
                        driver.find_element(By.XPATH, '//div[@aria-label="Like"]').click()
                        time.sleep(1)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(1)
            # 关注discord
            if len(dcord_url_list) > 0:
                for i in dcord_url_list:
                    driver.execute_script("window.open();")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(i)
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[-1])
                    invite_flag = checkElement('//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/section/div[2]/button')
                    if invite_flag:
                        driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/section/div[2]/button').click()
                    time.sleep(1)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
            # 搜索页面中是否有role
            text = driver.find_element(By.XPATH, "//*[text()]")
            role = "role"
            if role in text.text:
                print("need role, close page")
                print(driver.current_url)
                fp_role = open('need_role.txt', 'a', encoding='utf-8')
                fp_role.write(driver.current_url + '\n')
                fp_role.close()
                driver.close()
                return
            fp1 = open('can_auto.txt', 'a', encoding='utf-8')
            fp1.write(driver.current_url + '\n')
            fp1.close()
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(5)
            Success_flag = checkElement('//div[@class="card rounded-0 bg-success no-border"]')
            if not Success_flag:
                print(driver.current_url)
                fp_role = open('need_submit.txt', 'a', encoding='utf-8')
                fp_role.write(driver.current_url + '\n')
                fp_role.close()
            # if driver.find_element(By.XPATH, '//*[@id="register-form"]/div[1]/div[1]/div[1]').text == 'Registered':
            #     driver.close()
            driver.close()
            return
        except Exception as e:
            print(f'register失败，原因是：{e}')


def check_winning(chrome_account):
    driver = launchSeleniumWebdriver(chrome_account)
    driver.get('https://www.premint.xyz/collectors/entries/')
    flag = False
    fail_count = 0
    # 可以有更好的判断数量的方式
    time.sleep(120)
    for i in range(1, 100):
        try:
            status = driver.find_element(By.XPATH, f'//*[@id="st-container"]/div/div/div/div[2]/div[3]/div/div[2]/div[{str(i)}]/div/div[1]/a/div').text
        except:
            break
        if status == "📝  You're registered!":
            pass
        elif status in ["⛔  You were not selected!", "⛔  Sorry"]:
            flag = True
            fail_count += 1
            driver.find_element(By.XPATH, f'//*[@id="st-container"]/div/div/div/div[2]/div[3]/div/div[2]/div[{str(i)}]/div/div[1]/a/input').click()
        else:
            item = driver.find_element(By.XPATH, f'//*[@id="st-container"]/div/div/div/div[2]/div[3]/div/div[2]/div[{str(i)}]/div/div[2]/a').text
            winnner_message = f'{chrome_account}的{item}中奖了'
            print(winnner_message)
            fp1 = open('winner_list.txt', 'a', encoding='utf-8')
            fp1.write(winnner_message + '\n')
            fp1.close()

    if flag:
        driver.find_element(By.XPATH, '//*[@id="st-container"]/div/div/div/div[2]/div[3]/button').click()
        driver.switch_to.alert.accept()
        time.sleep(fail_count * 20)
    driver.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # auto_chrome_account_list = ['Profile 1', 'Profile 2', 'Profile 3', 'Profile 5', 'Profile 7', 'Profile 8', 'Profile 9',
    #                             'Profile 10', 'Profile 11', 'Profile 12', 'Profile 13', 'Profile 14', 'Profile 15', 'Profile 16', 'Profile 18',
    #                             'Profile 19', 'Profile 20', 'Profile 21', 'Profile 23', 'Profile 24', 'Profile 25', 'Profile 26', 'Profile 27', 'Profile 28',
    #                             'Profile 29', 'Profile 30', 'Profile 31', 'Profile 32', 'Profile 33', 'Profile 34', 'Profile 35',
    #                             'Profile 36']
    auto_chrome_account_list = ['Profile 3', 'Profile 5', 'Profile 7', 'Profile 8', 'Profile 9',
                                'Profile 10', 'Profile 11', 'Profile 12', 'Profile 13', 'Profile 14', 'Profile 15', 'Profile 16', 'Profile 18',
                                'Profile 19', 'Profile 20', 'Profile 21', 'Profile 23', 'Profile 24', 'Profile 25', 'Profile 26', 'Profile 27', 'Profile 28',
                                'Profile 29', 'Profile 30', 'Profile 31', 'Profile 32', 'Profile 33', 'Profile 34', 'Profile 35',
                                'Profile 36']
    # for account in auto_chrome_account_list:
    #     check_winning(account)
    for chrome_account in auto_chrome_account_list:
        print('开始' + chrome_account)
        driver = launchSeleniumWebdriver(chrome_account)
        driver.implicitly_wait(5)
        driver.get('https://www.premint.xyz/home/')
        # connectDiscord()
        # conncetMetaMask()
        # 读取url列表
        fp = open('premint_url.txt', 'r', encoding='utf-8')
        url_list = fp.readlines()
        fp.close()

        for i in range(0, len(url_list)):
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url_list[i])
            register(i)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
        driver.quit()
    time.sleep(60000)