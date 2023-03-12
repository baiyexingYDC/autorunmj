import random
import string
import time
from loguru import logger
import pyautogui
from datetime import datetime

from solusion.guiOperate import GuiOperate
from solusion.guiOperate.RateLimitedExcept import RateLimitedExcept
from solusion.guiOperate.VerifyExcept import VerifyExcept

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 拼接日志文件名称
log_filename = f'file_{current_date}.log'

# 添加日志处理器
logger.add(log_filename)

# 定义一个变量来控制循环
running = True

batch = 10

tail = random.randint(1, 999999)

name = "default"

run_inv = 130

# 使用try-except语句来捕获键盘中断异常
try:
    # 当running为True时，循环执行函数
    with open("url.txt", 'r') as f:
        for line in f:
            invite_url = line.strip()
            count = 0
            while running:
                count += 1
                try:
                    num_letters = random.randint(4, 10)
                    name_pre = ''.join(random.choice(string.ascii_letters) for _ in range(num_letters))
                    name = name_pre + str(tail)
                    logger.debug(f"邀请链接={invite_url}，用户名={name}")

                    # 配置
                    pyautogui.PAUSE = random.uniform(0.3, 0.7)
                    pyautogui.FAILSAFE = True
                    GuiOperate.pre_check()
                    # 录入用户名，破解验证
                    GuiOperate.click("model/browser/browser.png")
                    GuiOperate.open_inprivate()
                    GuiOperate.load_url(invite_url)
                    GuiOperate.register(name)
                    GuiOperate.solv_hCapcha(1)
                    GuiOperate.get_token()
                    GuiOperate.write_token(name)
                    time.sleep(run_inv)
                    if count == batch:
                        break
                except VerifyExcept as e:
                    count -= 1
                    screenName = f"{name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
                    logger.error(f"错误截图名称:{screenName}")
                    pyautogui.screenshot(f"error_screenshot/{screenName}.png")
                    logger.error(e)
                    logger.debug("验证异常")
                    time.sleep(run_inv)
                    continue
                except RateLimitedExcept as e:
                    count -= 1
                    screenName = f"{name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
                    logger.error(f"错误截图名称:{screenName}")
                    pyautogui.screenshot(f"error_screenshot/{screenName}.png")
                    logger.error(e)
                    logger.debug("访问受限!")
                    time.sleep(run_inv)
                    continue
                except Exception as e:
                    logger.error(e)
                    if "browser" in str(e):
                        count -= 1
                        screenName = f"{name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
                        logger.error(f"错误截图名称:{screenName}")
                        pyautogui.screenshot(f"error_screenshot/{screenName}.png")
                        logger.error("关闭浏览器窗口并继续")
                        GuiOperate.close_browser()
                        time.sleep(run_inv)
                        continue
                    else:
                        raise e
except KeyboardInterrupt:
    # 当按下ctrl+c时，设置running为False并退出循环
    logger.debug("程序手动停止")
except Exception as e:
    logger.error(e)
    screenName = f"{name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    logger.error(f"错误截图名称:{screenName}")
    pyautogui.screenshot(f"error_screenshot/{screenName}.png")
    logger.error("程序异常停止!")

