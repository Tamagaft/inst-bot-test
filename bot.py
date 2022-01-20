import pickle
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class InstagramBot():
    
    def __init__(self,username, password, options):
        self.username = username
        self.password = password
        #self.browser = webdriver.Chrome(Service("browsers/chromedriver"), options=options)
        self.browser = webdriver.Chrome("browsers/chromedriver", options=options)

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def login(self):
        browser = self.browser

        browser.get("https://www.instagram.com/")
        browser.implicitly_wait(5)
        time.sleep(random.randrange(1, 4))

        username_input = browser.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys(self.username)
        time.sleep(random.randrange(1, 3))

        password_input = browser.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        browser.implicitly_wait(5)

        print(f"Logged in {self.username} account")
        time.sleep(random.randrange(3, 6))
        time.sleep(10)

    def save_cookie(self):
        browser = self.browser
        self.login()
        pickle.dump(browser.get_cookies(), open(f"cookies/{self.username}_cookies", "wb"))
        print(f"Saved {self.username} cookies")

    def authenticate(self):
        browser = self.browser

        browser.get("https://www.instagram.com/")
        for cookie in pickle.load(open(f"cookies/{self.username}_cookies", "rb")):
            browser.add_cookie(cookie)

        print(f"Loaded {self.username} cookies")

        time.sleep(3)
        browser.refresh()

        browser.implicitly_wait(5)
        time.sleep(random.randrange(1, 3))

    def get_tag_users(self, tag):
        browser = self.browser

        try:
            browser.get(f"https://www.instagram.com/explore/tags/{tag}/")

            print("Scrolling photos")
            for i in range(5):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))

            print("getting posts links")
            hrefs = browser.find_elements(By.TAG_NAME, 'a')
            posts = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            print("saving users")
            print(len(posts))
            users = set()
            i = 0
            for e in posts:
                browser.get(e)
                browser.implicitly_wait(5)
                time.sleep(random.randrange(2, 4))

                user = browser.find_element(By.CLASS_NAME, 'yWX7d')
                users.add(user.text)

            print(f"gathered {len(users)} users")

            return list(users)

        except Exception as ex:
            print(ex)
        finally:
            self.close_browser()

    def subscribe_on_account(self, user):
        browser = self.browser

        browser.get(f"https://www.instagram.com/{user}/")
        browser.implicitly_wait(5)
        time.sleep(random.randrange(1, 3))

        browser.find_element(By.CLASS_NAME, "jIbKX").click()
        print(f"subscribed on {user}")

    def like_post(self, url):
        browser = self.browser

        try:
            browser.get(url)

            path = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
            if self.xpath_exists(path):
                browser.find_element(By.XPATH, path).click()
                print("post liked")

        except Exception as ex:
            print(ex)

        finally:
            self.close_browser()

    def unsubscribe_from_all(self):
        browser = self.browser

        browser.get(f"https://www.instagram.com/{self.username}/")
        browser.implicitly_wait(5)
        time.sleep(random.randrange(1, 3))

        path = "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a"

        if self.xpath_exists(path):
            following_button = browser.find_element(By.XPATH, path)

            following_button.click()
            browser.implicitly_wait(5)

            following_div_block = browser.find_element(By.CLASS_NAME, "PZuss")
            following_users = following_div_block.find_elements(By.TAG_NAME, "li")

            print("starting unsubscribing")
            for user in following_users:

                user.find_element(By.CLASS_NAME, "_8A5w5").click()
                browser.implicitly_wait(3)
                time.sleep(random.randrange(1, 2))

                browser.find_element(By.XPATH, "/html/body/div[7]/div/div/div/div[3]/button[1]").click()

                #time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(2, 4))



