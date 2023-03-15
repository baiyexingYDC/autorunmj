import re
import time
import random
from datetime import datetime

import pytesseract
from loguru import logger

import pyautogui

import settings
from RateLimitedExcept import RateLimitedExcept
from VerifyExcept import VerifyExcept
from utils.CaptchaResolver import CaptchaResolver
from utils.imageUtils import resize_base64_image

CONFIG = settings.load_config()
settings.create_dir()
model_path = CONFIG["model_path"]

def pre_check():
    shu = pyautogui.locateOnScreen(model_path + "/shurufa.png")
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
        if retry_count == 60:
            logger.error(f"模板{model_path}左击超时.......")
            raise Exception(f"模板{model_path}左击超时.......")

def right_click(model_path):
    retry_count = 0
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
        if browser is not None:
            x, y = pyautogui.center(browser)
            pyautogui.moveTo(x, y, duration=0.2)
            # pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeOutQuad)
            pyautogui.rightClick()
            logger.debug(f"模板{model_path}的位置{browser}")  # 打印 r 的值
        retry_count += 1
        if retry_count == 60:
            logger.error(f"模板{model_path}右击超时.......")
            raise Exception(f"模板{model_path}右击超时.......")

def random_click(model_path, random_x, random_y):
    retry_count = 0
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
        if browser is not None:
            x, y = pyautogui.center(browser)
            pyautogui.moveTo(x + random_x, y + random_y, duration=0.2)
            # pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeOutQuad)
            pyautogui.click()
            logger.debug(f"模板{model_path}的位置{browser}")  # 打印 r 的值
        retry_count += 1
        if retry_count == 60:
            logger.error(f"模板{model_path}点击超时.......")
            raise Exception(f"模板{model_path}点击超时.......")

def move_to_screen(model_path):
    region = get_region(model_path)
    pyautogui.moveTo(pyautogui.center(region))

def get_region(model_path):
    retry_count = 0
    browser = None  # 初始化一个变量 r
    while browser is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
        if browser is not None:
            return browser
        retry_count += 1
        if retry_count == 60:
            logger.error(f"模板{model_path}位置获取超时.......")
            raise Exception(f"模板{model_path}点击超时.......")

def get_region_now(model_path):
    browser = pyautogui.locateOnScreen(model_path, confidence=0.8)  # 使用 locateOnScreen() 函数找到模板图片的位置，并赋值给 r
    if browser is not None:
        return browser


def load_url(url):
    click(model_path + "/browser/browser-search.png")
    pyautogui.write(url, interval=0.03)
    pyautogui.click()
    pyautogui.press("enter")



def open_inprivate():
    pyautogui.hotkey("ctrl", "shift", "n")


def register(name):
    click(model_path + "/browser/input.png")
    pyautogui.write(name, interval=0.06)
    click(model_path + "/browser/continue.png")
    # 点击我是人类
    random_click(model_path + "/browser/hCapcha.png", random.randint(-60, 60), random.randint(-25, 25))

def check_verify(hCapcha_retry_time):
    retry = None

    retry_count = 0
    # 判断是否需要下一个
    while retry is None:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        retry = pyautogui.locateOnScreen(model_path + "/browser/check-next.png", confidence=0.8)
        if retry is not None:
            logger.debug(f"挑战重新进行下一个......")
            click(model_path + "/browser/check-next.png")
            solv_hCapcha(hCapcha_retry_time)
            return
        retry_count += 1
        if retry_count == 2:
            logger.debug(f"挑战未找到下一个验证！")
            break
        retry = None  # 将 r 设为 None，继续循环

    click(model_path + "/browser/check.png")

    retry_count = 0
    # 判断是否需要再试一次
    while True:  # 当 r 为 None 时，循环执行以下代码
        time.sleep(0.5)
        logger.debug(f"循环检测第{retry_count}次")
        try_again = pyautogui.locateOnScreen(model_path + "/browser/try-again.png", confidence=0.9)
        # check_skip = pyautogui.locateOnScreen(model_path + "/browser/check-skip.png", confidence=0.9)
        hCapcha = pyautogui.locateOnScreen(model_path + "/browser/hCapcha.png", confidence=0.8)
        check = pyautogui.locateOnScreen(model_path + "/check/phone.png", confidence=0.8)
        success = pyautogui.locateOnScreen(model_path + "/browser/success.png", confidence=0.8)
        re_email = pyautogui.locateOnScreen(model_path + "/browser/success-email.png", confidence=0.8)
        rare_limit = pyautogui.locateOnScreen(model_path + "/browser/rare-limit.png", confidence=0.9)
        conti = pyautogui.locateOnScreen(model_path + "/browser/continue.png", confidence=0.8)
        if try_again is not None:
            time.sleep(1.5)
            logger.debug(f"挑战重新进行识别......")
            solv_hCapcha(hCapcha_retry_time)
            break
        elif conti is not None:
            logger.debug("验证结束，回到了登录页，结束本次任务......")
            close_browser()
            raise VerifyExcept("验证结束，回到了登录页，结束本次任务......")
        elif hCapcha is not None:
            if hCapcha_retry_time <= 3:
                x, y = pyautogui.center(hCapcha)
                pyautogui.moveTo(x, y, duration=0.2)
                # pyautogui.moveTo(x, y, duration=0.3, tween=pyautogui.easeOutQuad)
                pyautogui.click()
                retry_count += 1
                logger.debug(f"验证不通过，重新识别")  # 打印 r 的值
                click(model_path + "/browser/hCapcha.png")
                solv_hCapcha(hCapcha_retry_time)
                break
            else:
                logger.debug("重试验证次数达到上限！...")
                raise Exception("重试验证次数达到上限！...")
        elif check is not None:
            logger.debug("触发风控！切换vpn节点并结束本次任务......")
            close_browser()
            change_vpn()
            raise VerifyExcept("触发风控！切换vpn节点并结束本次任务......")
        elif rare_limit is not None:
            logger.debug("触发风控！关闭浏览器跳过本次任务......")
            close_browser()
            raise RateLimitedExcept("触发风控！关闭浏览器跳过本次任务......")
        elif success is not None:
            logger.debug("验证通过,生日快乐！")
            break
        elif re_email is not None:
            logger.debug("验证通过,认证邮箱")
            break
        retry_count += 1


def close_browser():
    click(model_path + "/browser/browser-close.png")
    time.sleep(0.3)
    pyautogui.hotkey("win", "m")


def change_vpn():
    right_click(model_path + "/vpn_node/ico.png")
    move_to_screen(model_path + "/vpn_node/server-list.png")
    random_click(model_path + "/vpn_node/vpn.png", 0, random.randint(-114, 114))

def solv_hCapcha(hCapcha_retry_time):
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
        # 文本识别错误 点击跳过
        pyautogui.screenshot(f"error_screenshot/not-recognized-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
        click(model_path + "/browser/check-skip.png")
        solv_hCapcha(hCapcha_retry_time)
        logger.error('count not get captcha recognized indices')
    else:
        logger.debug(recognized_results)

        recognized_indices = [i for i, x in enumerate(recognized_results) if x]

        logger.debug(recognized_indices)
        if len(recognized_indices) == 0:
            click(model_path + "/browser/check-skip.png")
            solv_hCapcha(hCapcha_retry_time)
        else:
            # 选中识别后的图片
            click_img(recognized_indices)

            check_verify(hCapcha_retry_time)





def get_token():
    success = pyautogui.locateOnScreen(model_path + "/browser/success.png", confidence=0.8)
    # re_email = pyautogui.locateOnScreen(model_path + "/browser/success-email.png", confidence=0.8)
    if success:
        # 输入年月日
        click(model_path + "/browser/check-year.png")
        pyautogui.write("199" + str(random.randint(1, 9)))

        month = get_region(model_path + "/browser/check-month.png")
        click(model_path + "/browser/check-month.png")
        pyautogui.write(str(random.randint(1, 12)))
        pyautogui.moveTo(month[0] + 80, month[1] - 20, duration=0.1, tween=pyautogui.easeOutQuad)
        pyautogui.click()

        click(model_path + "/browser/check-day.png")
        pyautogui.write(str(random.randint(1, 20)))
        click(model_path + "/browser/check-done.png")

    success_email = get_region(model_path + "/browser/success-email.png")
    pyautogui.moveTo(success_email[0] - 100, success_email[1])
    pyautogui.click()

    # 输入prompt 并接受协议
    click(model_path + "/browser/channal-message.png")
    pyautogui.write("/i", interval=random.uniform(0.07, 0.1))
    click(model_path + "/browser/tab-prompt.png")
    pyautogui.write("a cute girl", interval=random.uniform(0.07, 0.1))
    pyautogui.press("enter")
    click(model_path + "/browser/channal-accept toS.png")

    # 从控制台获取token
    pyautogui.press('f12')
    click(model_path + "/browser/application.png")
    click(model_path + "/browser/filter.png")
    pyautogui.write("token", interval=0.03)
    token = get_region(model_path + "/browser/token.png")
    x, y = pyautogui.center(token)
    pyautogui.moveTo(x + 735, y + 15)
    pyautogui.doubleClick()
    pyautogui.hotkey("ctrl", "c")
    close_browser()



def get_question():
    region = get_region(model_path + "/browser/click-every.png")
    # pyautogui.moveTo(region[0], region[1], duration=0.2, tween=pyautogui.easeOutQuad)
    # 文本识别
    im = pyautogui.screenshot('temp/question.png', region=(region[0], region[1], 411, 85))
    text = pytesseract.image_to_string(im, lang='chi_sim')
    text = re.sub("\s+", "", text)
    logger.debug(f"识别文本:{text}")
    return text


def get_img_base64():
    region = get_region(model_path + "/browser/click-every.png")
    x, y = region[0], region[1]
    time.sleep(1.5)
    count = 0
    while True:
        time.sleep(0.5)
        l = pyautogui.locateOnScreen(model_path + "/browser/hCapcha-loading.png", confidence=0.6)
        if l is None or count == 20:
            logger.debug("验证码加载完毕!")
            break
        count += 1

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
    region = get_region(model_path + "/browser/click-every.png")
    x, y = region[0], region[1]
    count = 0  # 增加一个变量来记录循环的次数
    # 使用循环遍历每一行和每一列的图像
    for i in range(3):
        y1 = y + 177 + i * 194  # 计算每一行的y坐标
        for j in range(3):
            x1 = x + j * 194  # 计算每一列的x坐标
            if count in result:
                pyautogui.moveTo(x1 + 60 + random.randint(10, 90), y1 + 60 + random.randint(10, 90), duration=0.2, tween=pyautogui.easeOutQuad)
                pyautogui.click()
            count += 1


def write_token(name):
    pyautogui.PAUSE = 0.3
    click(model_path + "/wps_ico.png")

    excel_name = get_region(model_path + "/excel_name.png")
    pyautogui.moveTo(excel_name)
    pyautogui.click()
    pyautogui.press("f2")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(name)

    excel_token = get_region(model_path + "/excel_token.png")
    pyautogui.moveTo(excel_token)
    pyautogui.click()
    pyautogui.press("f2")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.scroll(-20)
    pyautogui.hotkey("ctrl", "s")
    click(model_path + "/excel-close.png")
    # pyautogui.rightClick()
    # click(model_path + "/paste.png")
    # time.sleep(1)
    # pyautogui.hotkey("alt", "esc")


def test():
    im = pyautogui.screenshot('temp/question.png', region=(1452, 797, 411, 85))
    text = pytesseract.image_to_string(im, lang='chi_sim')
    text = re.sub("\s+", "", text)
    logger.debug(f"识别文本:{text}")
