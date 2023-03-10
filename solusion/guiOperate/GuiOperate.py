import re
import time
import random

import pytesseract
from loguru import logger

import pyautogui

from utils.CaptchaResolver import CaptchaResolver
from utils.imageUtils import resize_base64_image

pytesseract.pytesseract.tesseract_cmd = r'D:\soft\tesseractocr\tesseract.exe'


def click(model_path):
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        try:  # 尝试执行以下代码
            browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
            x, y = pyautogui.center(browser)
            pyautogui.moveTo(x, y, duration=0.3)
            # pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeOutQuad)
            pyautogui.click()
            time.sleep(0.5)
            logger.debug(f"模板{model_path}的位置{browser}")  # 打印 r 的值
        except Exception as e:  # 如果发生异常，执行以下代码
            browser = None  # 将 r 设为 None，继续循环


def get_region(model_path):
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        try:  # 尝试执行以下代码
            browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
            time.sleep(0.5)
        except Exception as e:  # 如果发生异常，执行以下代码
            browser = None  # 将 r 设为 None，继续循环
    return browser


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


def solv_hCapcha():
    # 点击我是人类
    click("model/hCapcha.png")
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
    # while retry is None:  # 当 r 为 None 时，循环执行以下代码
    #     try:  # 尝试执行以下代码
    #         retry = pyautogui.locateOnScreen("model/try-again.png", confidence=0.8)
    #         retry_count += 1
    #         if retry_count == 4:
    #             retry = "done"
    #         time.sleep(0.5)
    #     except Exception as e:  # 如果发生异常，执行以下代码
    #         retry = None  # 将 r 设为 None，继续循环


def get_token():
    tokenText = ""
    success = get_region("model/success.png")
    if success:
        pyautogui.press('f12')
        click("model/application.png")
        click("model/filter.png")
        pyautogui.write("token", interval=0.03)
        token = get_region("model/token.png")
        x, y = pyautogui.center(token)
        pyautogui.moveTo(x + 430, y + 15)
        pyautogui.doubleClick()
        pyautogui.hotkey("ctrl", "c")


def get_question():
    region = get_region("model/click-every.png")
    pyautogui.moveTo(region[0], region[1], duration=0.4, tween=pyautogui.easeOutQuad)
    # 文本识别
    im = pyautogui.screenshot('temp/question.png', region=(region[0], region[1], 355, 55))
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
                pyautogui.moveTo(x1 + 60, y1 + 60, duration=0.4, tween=pyautogui.easeOutQuad)
                pyautogui.click()
            count += 1


def write_token():
    click("model/wps_ico.png")
    excelFlag = get_region("model/excel_flag.png")
    pyautogui.moveTo(excelFlag)
    pyautogui.rightClick()
    click("model/paste.png")


def test():
    # pyautogui.write("token", interval=0.03)
    token = get_region("model/token.png")
    x, y = pyautogui.center(token)
    pyautogui.moveTo(x + 430, y + 15)
    pyautogui.doubleClick()
    pyautogui.hotkey("ctrl", "c")
