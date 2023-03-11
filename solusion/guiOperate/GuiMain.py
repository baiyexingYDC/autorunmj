import random
import time
from loguru import logger
import pyautogui
from datetime import datetime

from solusion.guiOperate import GuiOperate

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 拼接日志文件名称
log_filename = f'file_{current_date}.log'

# 添加日志处理器
logger.add(log_filename)

# 定义一个变量来控制循环
running = True

count = 7

# 使用try-except语句来捕获键盘中断异常
try:
    # 当running为True时，循环执行函数
    while running:
        invite_url = "https://discord.gg/arPcQVA7JV"
        name = "say-girl-" + str(count)
        logger.debug(f"邀请链接={invite_url}，用户名={name}")

        #配置
        pyautogui.PAUSE = random.uniform(0.3, 0.7)
        pyautogui.FAILSAFE = True
        GuiOperate.pre_check()
        # 录入用户名，破解验证
        GuiOperate.click("model/browser.png")
        GuiOperate.open_inprivate()
        GuiOperate.load_url(invite_url)
        GuiOperate.register(name)
        GuiOperate.solv_hCapcha()
        GuiOperate.get_token()
        GuiOperate.write_token(name)

        if count == 10:
            break
        count += 1
        time.sleep(120)
except KeyboardInterrupt:
    # 当按下ctrl+c时，设置running为False并退出循环
    running = False
    logger.debug("程序手动停止")
except Exception as e:
    running = False
    logger.error(e)
    logger.error("程序异常停止!")
