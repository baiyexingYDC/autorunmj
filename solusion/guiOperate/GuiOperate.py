import re
import time
import random

import pytesseract
from loguru import logger

import pyautogui

from utils.CaptchaResolver import CaptchaResolver
from utils.imageUtils import resize_base64_image

pytesseract.pytesseract.tesseract_cmd = r'D:\soft\tesseractocr\tesseract.exe'


def pre_check():
    shu = pyautogui.locateOnScreen("model/shurufa.png")
    if shu:
        pyautogui.press("shift")


def click(model_path):
    retry_count = 0
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
        if browser is not None:
            x, y = pyautogui.center(browser)
            pyautogui.moveTo(x, y, duration=0.2)
            # pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeOutQuad)
            pyautogui.click()
            logger.debug(f"模板{model_path}的位置{browser}")  # 打印 r 的值
        retry_count += 1
        if retry_count == 120:
            logger.error(f"模板{model_path}点击超时.......")
            raise Exception(f"模板{model_path}点击超时.......")


def get_region(model_path):
    retry_count = 0
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
        if browser is not None:
            return browser
        if retry_count == 120:
            logger.error(f"模板{model_path}位置获取超时.......")
            raise Exception(f"模板{model_path}点击超时.......")


def load_url(url):
    click("model/browser-search.png")
    pyautogui.write(url, interval=0.03)
    pyautogui.click()
    pyautogui.press("enter")


def open_inprivate():
    pyautogui.hotkey("ctrl", "shift", "n")


def register(name):
    click("model/input.png")
    pyautogui.write(name, interval=0.06)
    click("model/continue.png")
    # 点击我是人类
    click("model/hCapcha.png")


def solv_hCapcha():
    # 获取问题
    question = get_question()
    # 获取图片并返回base64集合
    base64String = get_img_base64()
    # 验证码识别
    captcha_resolver = CaptchaResolver()
    # try to verify using API
    captcha_recognize_result = captcha_resolver.create_task(
        base64String,
        question
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

    recognized_indices = [i for i, x in enumerate(recognized_results) if x]

    logger.debug(recognized_indices)

    # 选中识别后的图片
    click_img(recognized_indices)

    click("model/check.png")

    retry = None

    retry_count = 0
    # 判断是否需要再试一次
    while retry is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        retry = pyautogui.locateOnScreen("model/try-again.png", confidence=0.8)
        if retry is not None:
            time.sleep(1.5)
            logger.debug(f"挑战重新进行识别......")
            solv_hCapcha()
        retry_count += 1
        if retry_count == 5:
            logger.debug(f"挑战未找到需要重试！")
            break
        retry = None  # 将 r 设为 None，继续循环


def get_token():
    success = get_region("model/success.png")
    time.sleep(1)
    if success:
        # 输入年月日
        click("model/check-year.png")
        pyautogui.write("199" + str(random.randint(1, 9)))

        month = get_region("model/check-month.png")
        click("model/check-month.png")
        pyautogui.write(str(random.randint(1, 12)))
        pyautogui.moveTo(month[0] + 80, month[1] - 20, duration=0.1, tween=pyautogui.easeOutQuad)
        pyautogui.click()

        click("model/check-day.png")
        pyautogui.write(str(random.randint(1, 20)))
        click("model/check-done.png")

        # 关闭认证邮箱
        success_email = get_region("model/success-email.png")
        pyautogui.moveTo(success_email[0] - 100, success_email[1])
        pyautogui.click()

        # 输入prompt 并接受协议
        click("model/channal-message.png")
        pyautogui.write("/imagine", interval=random.uniform(0.07, 0.1))
        time.sleep(0.4)
        pyautogui.write(" ")
        time.sleep(0.5)
        pyautogui.write("a cute girl", interval=random.uniform(0.07, 0.1))
        pyautogui.press("enter")
        click("model/channal-accept toS.png")

        # 从控制台获取token
        pyautogui.press('f12')
        click("model/application.png")
        click("model/filter.png")
        pyautogui.write("token", interval=0.03)
        token = get_region("model/token.png")
        x, y = pyautogui.center(token)
        pyautogui.moveTo(x + 735, y + 15)
        pyautogui.doubleClick()
        pyautogui.hotkey("ctrl", "c")
        click("model/browser-close.png")
        time.sleep(0.3)
        pyautogui.hotkey("win", "m")


def get_question():
    region = get_region("model/click-every.png")
    pyautogui.moveTo(region[0], region[1], duration=0.2, tween=pyautogui.easeOutQuad)
    # 文本识别
    im = pyautogui.screenshot('temp/question.png', region=(region[0], region[1], 411, 55))
    text = pytesseract.image_to_string(im, lang='chi_sim')
    text = re.sub("\s+", "", text)
    logger.debug(f"识别文本:{text}")
    return text


def get_img_base64():
    region = get_region("model/click-every.png")
    x, y = region[0], region[1]

    resized_single_captcha_base64_strings = []
    count = 1  # 增加一个变量来记录循环的次数
    # 使用循环遍历每一行和每一列的图像
    for i in range(3):
        y1 = y + 177 + i * 194  # 计算每一行的y坐标
        for j in range(3):
            x1 = x + j * 194  # 计算每一列的x坐标
            # pyautogui.moveTo(x1, y1, duration=0.2, tween=pyautogui.easeOutQuad) # 移动到对应的图像位置
            pyautogui.screenshot("temp/captcha_%d.jpg" % (count,), region=(x1, y1, 175, 175))
            resized_single_captcha_base64_string = resize_base64_image(
                "temp/captcha_%d.jpg" % (count,), (100, 100))
            resized_single_captcha_base64_strings.append(resized_single_captcha_base64_string)
            count += 1
    logger.debug(resized_single_captcha_base64_strings)
    return resized_single_captcha_base64_strings


def click_img(result):
    region = get_region("model/click-every.png")
    x, y = region[0], region[1]
    count = 0  # 增加一个变量来记录循环的次数
    # 使用循环遍历每一行和每一列的图像
    for i in range(3):
        y1 = y + 177 + i * 194  # 计算每一行的y坐标
        for j in range(3):
            x1 = x + j * 194  # 计算每一列的x坐标
            if count in result:
                pyautogui.moveTo(x1 + 60, y1 + 60, duration=0.2, tween=pyautogui.easeOutQuad)
                pyautogui.click()
            count += 1


def write_token(name):
    pyautogui.PAUSE = 0.1
    click("model/wps_ico.png")

    excel_name = get_region("model/excel_name.png")
    pyautogui.moveTo(excel_name)
    pyautogui.click()
    pyautogui.press("f2")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(name)

    excel_token = get_region("model/excel_token.png")
    pyautogui.moveTo(excel_token)
    pyautogui.click()
    pyautogui.press("f2")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "v")
    # pyautogui.rightClick()
    # click("model/paste.png")
    pyautogui.hotkey("alt", "esc")


def test():
    time.sleep(5)
    pyautogui.hotkey("win", "m")