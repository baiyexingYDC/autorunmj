import re
import time
import random

import requests
from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from CaptchaResolver import CaptchaResolver
from imgOperate import resize_base64_image
import undetected_chromedriver as uc

class Solution(object):
    def __init__(self, url):
        options = webdriver.EdgeOptions()
        options.add_argument("-inprivate")
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.browser = webdriver.Edge(options=options)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
              // 修改navigator.webdriver检测
              Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
              })
              // 修改window.navigator属性值
              window.navigator.chrome = {
                runtime: {},
                // etc.
              }
              // 修改插件信息
              const originalQuery = window.navigator.permissions.query;
              window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                  Promise.resolve({ state: Notification.permission }) :
                  originalQuery(parameters)
              );
            """
        })
        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 20)
        self.captcha_resolver = CaptchaResolver()

    def __del__(self):
        time.sleep(10)
        self.browser.close()

    def set_user_name(self, n, user_name_pre):
        # 邀请链接
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        input_ele = self.browser.find_element(By.NAME, "username")
        userName = user_name_pre + str(n)
        input_ele.send_keys(userName)
        time.sleep(1)
        # 定位到button type="submit"的元素
        button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        # 点击该元素
        button.click()

    @property
    def get_captcha_entry_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//iframe[contains(@title, "包含 hCaptcha 安全挑战复选框的小部件")]')))
        captcha_entry_iframe = self.browser.find_element(By.XPATH,
                                                         '//iframe[contains(@title, "包含 hCaptcha 安全挑战复选框的小部件")]')
        return captcha_entry_iframe

    def switch_to_captcha_entry_iframe(self) -> None:
        captcha_entry_iframe: WebElement = self.get_captcha_entry_iframe
        self.browser.switch_to.frame(captcha_entry_iframe)

    def get_captcha_content_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//iframe[contains(@title, "hCaptcha挑战的主要内容")]')))
        captcha_content_iframe = self.browser.find_element(By.XPATH,
                                                           '//iframe[contains(@title, "hCaptcha挑战的主要内容")]')
        return captcha_content_iframe

    def switch_to_captcha_content_iframe(self) -> None:
        captcha_content_iframe: WebElement = self.get_captcha_content_iframe()
        self.browser.switch_to.frame(captcha_content_iframe)

    def get_captcha_element(self) -> WebElement:
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".challenge-interface")))
        return self.browser.find_element(By.CSS_SELECTOR, ".challenge-interface")

    def trigger_captcha(self) -> None:
        time.sleep(5)
        self.switch_to_captcha_entry_iframe()

        captcha_entry = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#anchor #checkbox')))

        captcha_entry.click()

        self.switch_to_captcha_content_iframe()

        captcha_element: WebElement = self.get_captcha_element()
        if captcha_element.is_displayed:
            logger.debug('trigged captcha successfully')
        time.sleep(3)

    def get_captcha_target_text(self) -> str:
        captcha_target_name_element: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.prompt-text')))
        return captcha_target_name_element.text

    def verify_captcha(self):
        # 获取标题文本
        self.captcha_target_text = self.get_captcha_target_text()
        logger.debug(
            f'captcha_target_text {self.captcha_target_text}'
        )
        # 等待全部图片加载完毕
        single_captcha_elements = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.task-image .image-wrapper .image')))

        resized_single_captcha_base64_strings = []

        for i, single_captcha_element in enumerate(single_captcha_elements):
            single_captcha_element_style = single_captcha_element.get_attribute(
                'style')
            pattern = re.compile('url\("(https.*?)"\)')
            match_result = re.search(pattern, single_captcha_element_style)
            single_captcha_element_url = match_result.group(
                1) if match_result else None
            logger.debug(
                f'single_captcha_element_url {single_captcha_element_url}')
            with open("img/origin/captcha_%d.jpg" % (i,), 'wb') as f:
                f.write(requests.get(single_captcha_element_url).content)
            resized_single_captcha_base64_string = resize_base64_image(
                "img/origin/captcha_%d.jpg" % (i,), (100, 100))
            resized_single_captcha_base64_strings.append(
                resized_single_captcha_base64_string)

        logger.debug(
            f'length of single_captcha_element_urls {len(resized_single_captcha_base64_strings)}')

        # try to verify using API
        captcha_recognize_result = self.captcha_resolver.create_task(
            resized_single_captcha_base64_strings,
            self.captcha_target_text
        )
        if not captcha_recognize_result:
            logger.error('count not get captcha recognize result')
            return
        recognized_results = captcha_recognize_result.get(
            'solution', {}).get('objects')

        if not recognized_results:
            logger.error('count not get captcha recognized indices')
            return

        logger.debug(recognized_results)

        # click captchas
        recognized_indices = [i for i, x in enumerate(recognized_results) if x]
        logger.debug(f'recognized_indices {recognized_indices}')
        click_targets = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.task-image')))
        for recognized_index in recognized_indices:
            click_target: WebElement = click_targets[recognized_index]
            click_target.click()
            time.sleep(random.uniform(1, 3))

        # after all captcha clicked
        verify_button: WebElement = self.get_verify_button()
        if verify_button.is_displayed:
            verify_button.click()
            time.sleep(10)
            # check if succeed
            is_succeed = self.get_is_successful()
            if is_succeed:
                logger.debug('verifed successfully')
            else:
                self.trigger_captcha()
                self.verify_captcha()

    def get_verify_button(self) -> WebElement:
        verify_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.button-submit')))
        return verify_button

    def get_is_successful(self):
        self.switch_to_captcha_entry_iframe()
        anchor: WebElement = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '#anchor #checkbox'
        )))
        checked = anchor.get_attribute('aria-checked')
        logger.debug(f'checked {checked}')
        return str(checked) == 'true'